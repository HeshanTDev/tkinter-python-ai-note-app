import customtkinter as ctk

class SettingsPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=("white", "#141414"), **kwargs)
        
        self.label = ctk.CTkLabel(
            self, 
            text="Settings", 
            font=ctk.CTkFont(family="Inter", size=32, weight="bold"),
            text_color=("gray10", "#ffffff")
        )
        self.label.pack(pady=(40, 20), padx=40, anchor="w")
        
        self.card = ctk.CTkFrame(self, fg_color=("#f9f9f9", "#1e1e1e"), corner_radius=12, border_width=1, border_color=("gray85", "#2d2d2d"))
        self.card.pack(pady=10, padx=40, fill="x")

        self.info = ctk.CTkLabel(
            self.card, 
            text="AI Configuration\n\n"
                 "The application is currently configured via the .env file.\n"
                 "To update your settings:\n\n"
                 "• Open the .env file in the root directory\n"
                 "• Update OPENROUTER_API_KEY\n"
                 "• Choose a different model in OPENROUTER_MODEL\n\n"
                 "Restart the application to apply changes.",
            justify="left",
            font=ctk.CTkFont(family="Inter", size=14),
            text_color=("gray20", "gray70")
        )
        self.info.pack(pady=30, padx=30, anchor="w")
