"""
ui/settings_page.py
Settings page — manage AI model, theme, and app preferences.
API key is configured via .env file only (never displayed in the UI for security).
"""

import os
import customtkinter as ctk
from dotenv import load_dotenv, set_key
from pathlib import Path

from config.theme import COLORS, FONTS, RADIUS, SPACING
from config.settings import BASE_DIR


class SettingsPage(ctk.CTkFrame):
    """Application settings — model, theme, and app info."""

    ENV_PATH = BASE_DIR / ".env"

    AVAILABLE_MODELS = [
        "nvidia/nemotron-3-super-120b-a12b:free",
        "meta-llama/llama-3.1-8b-instruct:free",
        "anthropic/claude-3-haiku",
        "anthropic/claude-3.5-sonnet",
        "openai/gpt-4o-mini",
        "openai/gpt-4o",
        "google/gemini-2.0-flash-001",
    ]

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS["bg_editor"], **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ── Header ───────────────────────────────────────────────────────────
        ctk.CTkLabel(
            self,
            text="⚙️  Settings",
            font=ctk.CTkFont(family=FONTS["h1"][0], size=FONTS["h1"][1], weight="bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=40, pady=(36, 24))

        # ── Scrollable content area ──────────────────────────────────────────
        content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew", padx=32, pady=(0, 32))
        content.grid_columnconfigure(0, weight=1)

        row_idx = 0

        # ─────────────────────────────────────────────────────────────────────
        #  CARD 1: AI Model Selection
        # ─────────────────────────────────────────────────────────────────────
        model_card = self._card(content, "🤖  AI Model", row_idx)
        row_idx += 1

        ctk.CTkLabel(
            model_card,
            text="Choose the AI model for summarizing, explaining, and other AI tools.",
            font=ctk.CTkFont(family=FONTS["body_sm"][0], size=FONTS["body_sm"][1]),
            text_color=COLORS["text_muted"],
            anchor="w",
            wraplength=500,
        ).pack(fill="x", padx=24, pady=(0, 10))

        self.model_menu = ctk.CTkOptionMenu(
            model_card,
            values=self.AVAILABLE_MODELS,
            font=ctk.CTkFont(family=FONTS["body_sm"][0], size=FONTS["body_sm"][1]),
            fg_color=COLORS["bg_input"],
            button_color=(COLORS["border"][0], "#333333"),
            button_hover_color=COLORS["hover_nav"],
            text_color=COLORS["text_primary"],
            corner_radius=RADIUS["sm"],
            height=38,
        )
        self.model_menu.pack(fill="x", padx=24, pady=(0, 20))

        # ─────────────────────────────────────────────────────────────────────
        #  CARD 2: Appearance
        # ─────────────────────────────────────────────────────────────────────
        theme_card = self._card(content, "🎨  Appearance", row_idx)
        row_idx += 1

        ctk.CTkLabel(
            theme_card,
            text="Select the application color theme.",
            font=ctk.CTkFont(family=FONTS["body_sm"][0], size=FONTS["body_sm"][1]),
            text_color=COLORS["text_muted"],
            anchor="w",
        ).pack(fill="x", padx=24, pady=(0, 10))

        self.theme_var = ctk.StringVar(value="Dark")
        theme_row = ctk.CTkFrame(theme_card, fg_color="transparent")
        theme_row.pack(fill="x", padx=24, pady=(0, 20))

        for mode in ["Light", "Dark", "System"]:
            ctk.CTkRadioButton(
                theme_row,
                text=mode,
                variable=self.theme_var,
                value=mode,
                command=self._on_theme_change,
                font=ctk.CTkFont(family=FONTS["body"][0], size=FONTS["body"][1]),
                text_color=COLORS["text_primary"],
                fg_color=COLORS["accent"],
                hover_color=COLORS["accent_hover"],
                border_color=COLORS["border"],
            ).pack(side="left", padx=(0, 24))


        # ─────────────────────────────────────────────────────────────────────
        #  CARD 4: API Configuration Info
        # ─────────────────────────────────────────────────────────────────────
        api_card = self._card(content, "🔑  API Configuration", row_idx)
        row_idx += 1

        # Status indicator
        api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
        if api_key:
            status_text = "✅  API key is configured"
            status_color = COLORS["success"]
        else:
            status_text = "⚠️  No API key found"
            status_color = ("#d97706", "#fbbf24")

        self.api_status = ctk.CTkLabel(
            api_card,
            text=status_text,
            font=ctk.CTkFont(family=FONTS["body"][0], size=FONTS["body"][1], weight="bold"),
            text_color=status_color,
            anchor="w",
        )
        self.api_status.pack(fill="x", padx=24, pady=(0, 8))

        ctk.CTkLabel(
            api_card,
            text="Your API key is stored securely in the .env file.\n"
                 "To change it, edit the .env file in the project root:\n\n"
                 "  OPENROUTER_API_KEY=sk-or-v1-your-key-here\n"
                 "  OPENROUTER_MODEL=model-name\n\n"
                 "Get a free API key at openrouter.ai",
            font=ctk.CTkFont(family=FONTS["body_sm"][0], size=FONTS["body_sm"][1]),
            text_color=COLORS["text_muted"],
            anchor="w",
            justify="left",
            wraplength=500,
        ).pack(fill="x", padx=24, pady=(0, 20))

        # ─────────────────────────────────────────────────────────────────────
        #  CARD 5: About
        # ─────────────────────────────────────────────────────────────────────
        about_card = self._card(content, "ℹ️  About", row_idx)
        row_idx += 1

        ctk.CTkLabel(
            about_card,
            text="AI Notes App  •  v1.0.0\n"
                 "A smart writing companion powered by AI.\n\n"
                 "Built with Python, CustomTkinter, and OpenRouter API.",
            font=ctk.CTkFont(family=FONTS["body_sm"][0], size=FONTS["body_sm"][1]),
            text_color=COLORS["text_muted"],
            anchor="w",
            justify="left",
        ).pack(fill="x", padx=24, pady=(0, 20))

        # ─────────────────────────────────────────────────────────────────────
        #  Save Button
        # ─────────────────────────────────────────────────────────────────────
        btn_row = ctk.CTkFrame(content, fg_color="transparent")
        btn_row.grid(row=row_idx, column=0, sticky="ew", pady=(16, 8))

        self.save_status = ctk.CTkLabel(
            btn_row,
            text="",
            font=ctk.CTkFont(family=FONTS["caption"][0], size=FONTS["caption"][1]),
            text_color=COLORS["success"],
        )
        self.save_status.pack(side="left")

        ctk.CTkButton(
            btn_row,
            text="💾  Save Settings",
            width=160,
            height=40,
            corner_radius=RADIUS["sm"],
            font=ctk.CTkFont(family=FONTS["body"][0], size=FONTS["body"][1], weight="bold"),
            fg_color=(COLORS["accent"], COLORS["accent"]),
            hover_color=(COLORS["accent_hover"], COLORS["accent_hover"]),
            text_color=COLORS["text_white"],
            command=self._save_settings,
        ).pack(side="right")

        # Load current model
        self._load_current_model()

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _card(self, parent, title: str, row: int) -> ctk.CTkFrame:
        """Create a styled settings card."""
        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_card"],
            corner_radius=RADIUS["lg"],
            border_width=1,
            border_color=COLORS["border"],
        )
        card.grid(row=row, column=0, sticky="ew", pady=8)

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(family=FONTS["h3"][0], size=FONTS["h3"][1], weight="bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x", padx=24, pady=(20, 12))

        return card

    def _load_current_model(self):
        """Load the current model from .env."""
        load_dotenv(str(self.ENV_PATH), override=True)
        model = os.getenv("OPENROUTER_MODEL", self.AVAILABLE_MODELS[0])
        if model in self.AVAILABLE_MODELS:
            self.model_menu.set(model)
        else:
            self.model_menu.set(self.AVAILABLE_MODELS[0])

    def _save_settings(self):
        """Save model selection to .env file."""
        model = self.model_menu.get()
        env_path = str(self.ENV_PATH)

        if not Path(env_path).exists():
            Path(env_path).touch()

        set_key(env_path, "OPENROUTER_MODEL", model)
        load_dotenv(env_path, override=True)

        self.save_status.configure(text="Settings saved ✓", text_color=COLORS["success"])
        self.after(3000, lambda: self.save_status.configure(text=""))

    def _on_theme_change(self):
        """Apply the selected theme."""
        ctk.set_appearance_mode(self.theme_var.get())
