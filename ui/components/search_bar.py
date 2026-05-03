"""
ui/components/search_bar.py
Reusable search input with icon and debounced callback.
"""

import customtkinter as ctk
from config.theme import COLORS, FONTS, RADIUS


class SearchBar(ctk.CTkFrame):
    """A search input widget with a magnifying-glass icon and debounce."""

    def __init__(self, master, placeholder: str = "Search notes...",
                 on_search=None, debounce_ms: int = 300, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self._on_search = on_search
        self._debounce_ms = debounce_ms
        self._debounce_timer = None

        self.grid_columnconfigure(0, weight=1)

        # Container with icon + entry
        self.container = ctk.CTkFrame(
            self,
            fg_color=COLORS["bg_input"],
            corner_radius=RADIUS["lg"],
            border_width=1,
            border_color=COLORS["border"],
        )
        self.container.pack(fill="x")
        self.container.grid_columnconfigure(1, weight=1)

        # Icon label
        self.icon = ctk.CTkLabel(
            self.container,
            text="🔍",
            font=ctk.CTkFont(size=14),
            text_color=COLORS["text_muted"],
            width=30,
        )
        self.icon.grid(row=0, column=0, padx=(12, 0), pady=0)

        # Entry
        self.entry = ctk.CTkEntry(
            self.container,
            placeholder_text=placeholder,
            font=ctk.CTkFont(family=FONTS["body"][0], size=FONTS["body"][1]),
            height=40,
            fg_color="transparent",
            border_width=0,
            text_color=COLORS["text_primary"],
        )
        self.entry.grid(row=0, column=1, sticky="ew", padx=(4, 12), pady=4)
        self.entry.bind("<KeyRelease>", self._on_key)

    def _on_key(self, event=None):
        """Debounced key handler."""
        if self._debounce_timer is not None:
            self.after_cancel(self._debounce_timer)
        self._debounce_timer = self.after(self._debounce_ms, self._fire_search)

    def _fire_search(self):
        if self._on_search:
            self._on_search(self.entry.get())

    def get(self) -> str:
        """Return the current search text."""
        return self.entry.get()

    def clear(self):
        """Clear the search bar."""
        self.entry.delete(0, "end")
