import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, nav_callback, **kwargs):
        super().__init__(master, width=220, corner_radius=0, fg_color=("#f0f0f0", "#1a1a1a"), **kwargs)
        self.nav_callback = nav_callback

        self.grid_rowconfigure(4, weight=1)

        # Brand Header
        self.brand_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.brand_frame.grid(row=0, column=0, padx=20, pady=(40, 30), sticky="ew")
        
        self.logo_label = ctk.CTkLabel(
            self.brand_frame, 
            text="AI NOTES", 
            font=ctk.CTkFont(family="Inter", size=24, weight="bold"),
            text_color=("#1a1a1a", "#ffffff")
        )
        self.logo_label.pack(anchor="center")
        
        self.subtitle_label = ctk.CTkLabel(
            self.brand_frame,
            text="Smart writing companion",
            font=ctk.CTkFont(family="Inter", size=11),
            text_color=("gray50", "gray50")
        )
        self.subtitle_label.pack(anchor="center", pady=(0, 10))

        # Navigation Buttons
        self.notes_btn = ctk.CTkButton(
            self, 
            text="  My Notes", 
            image=None, # Placeholder for icons if needed
            command=lambda: self._on_nav_click("notes"),
            font=ctk.CTkFont(family="Inter", size=14, weight="normal"),
            height=45,
            corner_radius=8,
            fg_color="transparent",
            hover_color=("#e5e5e5", "#2d2d2d"),
            text_color=("gray10", "gray80"),
            anchor="w"
        )
        self.notes_btn.grid(row=1, column=0, padx=15, pady=5, sticky="ew")

        self.settings_btn = ctk.CTkButton(
            self, 
            text="  Settings", 
            command=lambda: self._on_nav_click("settings"),
            font=ctk.CTkFont(family="Inter", size=14, weight="normal"),
            height=45,
            corner_radius=8,
            fg_color="transparent",
            hover_color=("#e5e5e5", "#2d2d2d"),
            text_color=("gray10", "gray80"),
            anchor="w"
        )
        self.settings_btn.grid(row=2, column=0, padx=15, pady=5, sticky="ew")

        # Appearance Mode Toggle
        self.mode_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.mode_frame.grid(row=6, column=0, padx=20, pady=(5, 30), sticky="ew")
        
        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.mode_frame, 
            values=["System", "Light", "Dark"],
            command=self.change_appearance_mode_event,
            fg_color=("#e5e5e5", "#2d2d2d"),
            button_color=("#d1d1d1", "#3d3d3d"),
            button_hover_color=("#c5c5c5", "#4d4d4d"),
            text_color=("gray10", "gray90"),
            font=ctk.CTkFont(family="Inter", size=12)
        )
        self.appearance_mode_menu.pack(fill="x")
        self.appearance_mode_menu.set("Dark")

    def _on_nav_click(self, page_name):
        # Reset button styles
        self.notes_btn.configure(fg_color="transparent", text_color=("gray10", "gray80"))
        self.settings_btn.configure(fg_color="transparent", text_color=("gray10", "gray80"))
        
        # Set active style
        active_btn = self.notes_btn if page_name == "notes" else self.settings_btn
        active_btn.configure(fg_color=("#3b82f6", "#2563eb"), text_color="white")
        
        self.nav_callback(page_name)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
