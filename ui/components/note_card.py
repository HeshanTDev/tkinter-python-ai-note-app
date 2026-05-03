"""
ui/components/note_card.py
Reusable note list-item card with title preview, content snippet, and timestamp.
"""

import customtkinter as ctk
from config.theme import COLORS, FONTS, RADIUS


class NoteCard(ctk.CTkFrame):
    """A compact card that shows a note preview in the sidebar list."""

    def __init__(self, master, title: str, content: str, timestamp: str,
                 is_active: bool = False, on_click=None, **kwargs):
        
        bg = COLORS["bg_card_active"] if is_active else "transparent"
        border_c = COLORS["border_active"] if is_active else COLORS["border"]

        super().__init__(
            master,
            fg_color=bg,
            corner_radius=RADIUS["lg"],
            border_width=1,
            border_color=border_c,
            cursor="hand2",
            **kwargs,
        )

        self._on_click = on_click
        self._is_active = is_active

        self.grid_columnconfigure(0, weight=1)

        # ── Title row ────────────────────────────────────────────────────────
        title_text = self._truncate(title if title.strip() else "Untitled Note", 26)
        self.title_label = ctk.CTkLabel(
            self,
            text=title_text,
            font=ctk.CTkFont(family=FONTS["body"][0], size=FONTS["body"][1], weight="bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        )
        self.title_label.grid(row=0, column=0, sticky="ew", padx=14, pady=(12, 0))

        # ── Content preview ──────────────────────────────────────────────────
        snippet = self._truncate(content.replace("\n", " ").strip() or "No content yet", 50)
        self.snippet_label = ctk.CTkLabel(
            self,
            text=snippet,
            font=ctk.CTkFont(family=FONTS["caption"][0], size=FONTS["caption"][1]),
            text_color=COLORS["text_muted"],
            anchor="w",
        )
        self.snippet_label.grid(row=1, column=0, sticky="ew", padx=14, pady=(2, 0))

        # ── Timestamp ────────────────────────────────────────────────────────
        time_str = self._format_time(timestamp)
        self.time_label = ctk.CTkLabel(
            self,
            text=time_str,
            font=ctk.CTkFont(family=FONTS["caption"][0], size=10),
            text_color=COLORS["text_muted"],
            anchor="w",
        )
        self.time_label.grid(row=2, column=0, sticky="ew", padx=14, pady=(2, 10))

        # ── Bind click on the whole card ─────────────────────────────────────
        self._bind_recursive(self, "<Button-1>", self._handle_click)

        # ── Hover effect (only if not active) ────────────────────────────────
        if not is_active:
            self._bind_recursive(self, "<Enter>", self._on_enter)
            self._bind_recursive(self, "<Leave>", self._on_leave)

    # ── Event handlers ───────────────────────────────────────────────────────

    def _handle_click(self, event=None):
        if self._on_click:
            self._on_click()

    def _on_enter(self, event=None):
        self.configure(fg_color=COLORS["hover_card"])

    def _on_leave(self, event=None):
        self.configure(fg_color="transparent")

    # ── Helpers ──────────────────────────────────────────────────────────────

    @staticmethod
    def _truncate(text: str, max_len: int) -> str:
        return text[:max_len - 3] + "..." if len(text) > max_len else text

    @staticmethod
    def _format_time(iso_str: str) -> str:
        """Turn '2026-05-03T22:15:56.259' into '03 May 2026 • 22:15'."""
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(iso_str)
            return dt.strftime("%d %b %Y • %H:%M")
        except Exception:
            return iso_str[:16].replace("T", " ")

    @staticmethod
    def _bind_recursive(widget, event: str, handler):
        """Bind an event to a widget and all its children so clicks work everywhere."""
        widget.bind(event, handler)
        for child in widget.winfo_children():
            NoteCard._bind_recursive(child, event, handler)
