"""
ui/components/modal.py
Reusable modal dialog for AI previews, confirmations, etc.
"""

import customtkinter as ctk
from config.theme import COLORS, FONTS, RADIUS


class Modal(ctk.CTkToplevel):
    """A reusable modal dialog with header, scrollable body, and action buttons."""

    def __init__(self, parent, title: str = "Dialog", width: int = 620, height: int = 480):
        super().__init__(parent)

        self.title(title)
        self.geometry(f"{width}x{height}")
        self.transient(parent.winfo_toplevel())
        self.grab_set()
        self.resizable(True, True)

        # Center on parent
        self.update_idletasks()
        px = parent.winfo_toplevel().winfo_rootx()
        py = parent.winfo_toplevel().winfo_rooty()
        pw = parent.winfo_toplevel().winfo_width()
        ph = parent.winfo_toplevel().winfo_height()
        x = px + (pw - width) // 2
        y = py + (ph - height) // 2
        self.geometry(f"+{x}+{y}")

        self.configure(fg_color=COLORS["bg_modal"])

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ── Header ───────────────────────────────────────────────────────────
        self.header = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(family=FONTS["h2"][0], size=FONTS["h2"][1], weight="bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        )
        self.header.grid(row=0, column=0, sticky="ew", padx=28, pady=(24, 8))

        # ── Body area (textbox) ──────────────────────────────────────────────
        self.body = ctk.CTkTextbox(
            self,
            wrap="word",
            font=ctk.CTkFont(family=FONTS["body_lg"][0], size=FONTS["body_lg"][1]),
            fg_color=COLORS["bg_input"],
            text_color=COLORS["text_primary"],
            border_width=1,
            border_color=COLORS["border"],
            corner_radius=RADIUS["lg"],
        )
        self.body.grid(row=1, column=0, sticky="nsew", padx=28, pady=8)

        # ── Footer / button bar ──────────────────────────────────────────────
        self.footer = ctk.CTkFrame(self, fg_color="transparent")
        self.footer.grid(row=2, column=0, sticky="e", padx=28, pady=(8, 24))

    def set_body_text(self, text: str, readonly: bool = True):
        """Populate the body textbox."""
        self.body.configure(state="normal")
        self.body.delete("1.0", "end")
        self.body.insert("1.0", text)
        if readonly:
            self.body.configure(state="disabled")

    def add_button(self, text: str, command, style: str = "primary"):
        """Add a button to the footer. style = 'primary' | 'danger' | 'ghost'."""
        btn_cfg = {
            "primary": {
                "fg_color": (COLORS["success"], COLORS["success"]),
                "hover_color": (COLORS["success_hover"], COLORS["success_hover"]),
                "text_color": COLORS["text_white"],
            },
            "danger": {
                "fg_color": (COLORS["danger"], COLORS["danger"]),
                "hover_color": (COLORS["danger_hover"], COLORS["danger_hover"]),
                "text_color": COLORS["text_white"],
            },
            "ghost": {
                "fg_color": "transparent",
                "hover_color": COLORS["hover_card"],
                "text_color": COLORS["text_secondary"],
                "border_width": 1,
                "border_color": COLORS["border"],
            },
        }

        cfg = btn_cfg.get(style, btn_cfg["primary"])
        btn = ctk.CTkButton(
            self.footer,
            text=text,
            width=110,
            height=36,
            corner_radius=RADIUS["sm"],
            command=command,
            font=ctk.CTkFont(family=FONTS["body_sm"][0], size=FONTS["body_sm"][1], weight="bold"),
            **cfg,
        )
        btn.pack(side="right", padx=(8, 0))
        return btn
