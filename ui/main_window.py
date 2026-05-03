"""
ui/main_window.py
Application root window — manages sidebar navigation and page routing.
"""

import customtkinter as ctk
from config.settings import WINDOW_TITLE, WINDOW_SIZE, THEME_COLOR, APPEARANCE_MODE
from ui.sidebar import Sidebar
from ui.notes_page import NotesPage
from ui.ai_tools_page import AIToolsPage
from ui.settings_page import SettingsPage


class MainWindow(ctk.CTk):
    """Root application window with sidebar navigation."""

    def __init__(self):
        super().__init__()

        self.title(WINDOW_TITLE)

        # Center the window on screen
        width, height = map(int, WINDOW_SIZE.split("x"))
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.minsize(900, 600)

        ctk.set_appearance_mode(APPEARANCE_MODE)
        ctk.set_default_color_theme(THEME_COLOR)

        # Layout grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # sidebar
        self.grid_columnconfigure(1, weight=1)  # content

        # Sidebar
        self.sidebar = Sidebar(self, self.navigate)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Pages (lazy-ish — created once)
        self._notes_page = NotesPage(self)
        self._ai_tools_page = AIToolsPage(self, get_notes_page=lambda: self._notes_page)
        self._settings_page = SettingsPage(self)

        self.pages = {
            "notes":    self._notes_page,
            "ai_tools": self._ai_tools_page,
            "settings": self._settings_page,
        }

        self.current_page = None
        self.navigate("notes")

    def navigate(self, page_name: str):
        """Switch the visible page in the main content area."""
        if self.current_page:
            self.current_page.grid_forget()

        page = self.pages.get(page_name)
        if page:
            self.current_page = page
            self.current_page.grid(row=0, column=1, sticky="nsew")
