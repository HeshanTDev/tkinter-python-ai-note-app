"""
ui/sidebar.py
Application sidebar with navigation, branding, and appearance toggle.
"""

import customtkinter as ctk
from config.theme import COLORS, FONTS, RADIUS, SPACING


class Sidebar(ctk.CTkFrame):
    """Main navigation sidebar for the application."""

    NAV_ITEMS = [
        {"key": "notes",    "label": "📝  My Notes",   "row": 2},
        {"key": "ai_tools", "label": "✨  AI Tools",    "row": 3},
        {"key": "settings", "label": "⚙️  Settings",    "row": 4},
    ]

    def __init__(self, master, nav_callback, **kwargs):
        super().__init__(
            master,
            width=230,
            corner_radius=0,
            fg_color=COLORS["bg_sidebar"],
            **kwargs,
        )
        self.nav_callback = nav_callback
        self._buttons = {}  # key -> CTkButton

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)  # spacer pushes footer down

        # ── Brand ────────────────────────────────────────────────────────────
        brand = ctk.CTkFrame(self, fg_color="transparent")
        brand.grid(row=0, column=0, padx=SPACING["lg"], pady=(36, 8), sticky="ew")

        ctk.CTkLabel(
            brand,
            text="AI NOTES",
            font=ctk.CTkFont(family=FONTS["brand"][0], size=FONTS["brand"][1], weight="bold"),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w")

        ctk.CTkLabel(
            brand,
            text="Smart writing companion",
            font=ctk.CTkFont(family=FONTS["caption"][0], size=FONTS["caption"][1]),
            text_color=COLORS["text_muted"],
        ).pack(anchor="w", pady=(2, 0))

        # ── Divider ──────────────────────────────────────────────────────────
        ctk.CTkFrame(
            self, height=1, fg_color=COLORS["border"],
        ).grid(row=1, column=0, sticky="ew", padx=SPACING["lg"], pady=(16, 16))

        # ── Nav buttons ──────────────────────────────────────────────────────
        for item in self.NAV_ITEMS:
            btn = ctk.CTkButton(
                self,
                text=item["label"],
                command=lambda k=item["key"]: self._on_nav_click(k),
                font=ctk.CTkFont(family=FONTS["body"][0], size=FONTS["body"][1]),
                height=42,
                corner_radius=RADIUS["md"],
                fg_color="transparent",
                hover_color=COLORS["hover_nav"],
                text_color=COLORS["text_secondary"],
                anchor="w",
            )
            btn.grid(row=item["row"], column=0, padx=12, pady=3, sticky="ew")
            self._buttons[item["key"]] = btn

        # ── Footer: Appearance toggle ────────────────────────────────────────
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=6, column=0, padx=SPACING["lg"], pady=(8, 24), sticky="sew")

        ctk.CTkLabel(
            footer,
            text="Appearance",
            font=ctk.CTkFont(family=FONTS["caption"][0], size=FONTS["caption"][1]),
            text_color=COLORS["text_muted"],
        ).pack(anchor="w", pady=(0, 6))

        self.appearance_menu = ctk.CTkOptionMenu(
            footer,
            values=["System", "Light", "Dark"],
            command=self._change_appearance,
            fg_color=COLORS["bg_input"],
            button_color=(COLORS["border"][0], "#333333"),
            button_hover_color=COLORS["hover_nav"],
            text_color=COLORS["text_primary"],
            font=ctk.CTkFont(family=FONTS["body_sm"][0], size=FONTS["body_sm"][1]),
            corner_radius=RADIUS["sm"],
            height=32,
        )
        self.appearance_menu.pack(fill="x")
        self.appearance_menu.set("Dark")

        # Set initial active state
        self._set_active("notes")

    # ── Navigation ───────────────────────────────────────────────────────────

    def _on_nav_click(self, key: str):
        self._set_active(key)
        self.nav_callback(key)

    def _set_active(self, active_key: str):
        """Highlight the active nav button, reset others."""
        for key, btn in self._buttons.items():
            if key == active_key:
                btn.configure(
                    fg_color=(COLORS["accent"], COLORS["accent"]),
                    text_color=COLORS["text_white"],
                    hover_color=(COLORS["accent_hover"], COLORS["accent_hover"]),
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=COLORS["text_secondary"],
                    hover_color=COLORS["hover_nav"],
                )

    @staticmethod
    def _change_appearance(mode: str):
        ctk.set_appearance_mode(mode)
