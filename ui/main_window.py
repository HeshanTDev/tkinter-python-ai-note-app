import customtkinter as ctk
from config.settings import WINDOW_TITLE, WINDOW_SIZE, THEME_COLOR, APPEARANCE_MODE
from ui.sidebar import Sidebar
from ui.notes_page import NotesPage
from ui.settings_page import SettingsPage

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(WINDOW_TITLE)
        
        # Center the window
        width, height = map(int, WINDOW_SIZE.split('x'))
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        ctk.set_appearance_mode(APPEARANCE_MODE)
        ctk.set_default_color_theme(THEME_COLOR)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar = Sidebar(self, self.navigate)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.pages = {
            "notes": NotesPage(self),
            "settings": SettingsPage(self)
        }

        self.current_page = None
        self.navigate("notes")

    def navigate(self, page_name):
        if self.current_page:
            self.current_page.grid_forget()
            
        self.current_page = self.pages[page_name]
        self.current_page.grid(row=0, column=1, sticky="nsew")
