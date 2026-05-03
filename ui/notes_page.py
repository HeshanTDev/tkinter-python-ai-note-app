import customtkinter as ctk
import threading
from tkinter import messagebox
from services.note_service import NoteService
from services.ai_service import AIService
from services.export_service import ExportService

class NotesPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=3, uniform="group1")
        self.grid_rowconfigure(0, weight=1)

        self.current_note = None
        self._save_timer = None

        self._create_list_pane()
        self._create_editor_pane()
        self.load_notes()

    def _create_list_pane(self):
        self.list_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=("#f9f9f9", "#111111"))
        self.list_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_rowconfigure(2, weight=1)

        # Search section
        self.search_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        self.search_frame.grid(row=0, column=0, padx=20, pady=(30, 10), sticky="ew")
        
        self.search_entry = ctk.CTkEntry(
            self.search_frame, 
            placeholder_text="Search notes...",
            font=ctk.CTkFont(family="Inter", size=14),
            height=40,
            fg_color=("white", "#1e1e1e"),
            border_color=("gray80", "#2d2d2d"),
            border_width=1,
            corner_radius=10
        )
        self.search_entry.pack(fill="x")
        self.search_entry.bind("<KeyRelease>", self.on_search)

        self.new_btn = ctk.CTkButton(
            self.list_frame, 
            text="+  New Note", 
            command=self.create_new_note,
            font=ctk.CTkFont(family="Inter", size=14, weight="bold"),
            height=45,
            corner_radius=10,
            fg_color=("#3b82f6", "#2563eb"),
            hover_color=("#2563eb", "#1d4ed8"),
            text_color="white"
        )
        self.new_btn.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")

        self.scrollable_list = ctk.CTkScrollableFrame(self.list_frame, fg_color="transparent")
        self.scrollable_list.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))

    def _create_editor_pane(self):
        self.editor_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=("white", "#141414"))
        self.editor_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.editor_frame.grid_columnconfigure(0, weight=1)
        self.editor_frame.grid_rowconfigure(1, weight=1)

        # Top Bar
        self.top_bar = ctk.CTkFrame(self.editor_frame, height=80, fg_color="transparent")
        self.top_bar.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 10))
        
        self.title_entry = ctk.CTkEntry(
            self.top_bar, 
            placeholder_text="Untiltled Note", 
            font=ctk.CTkFont(family="Inter", size=28, weight="bold"),
            border_width=0,
            fg_color="transparent",
            text_color=("gray10", "#ffffff")
        )
        self.title_entry.pack(side="left", fill="x", expand=True, padx=(0, 20))
        self.title_entry.bind("<KeyRelease>", self._schedule_save)

        self.action_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        self.action_frame.pack(side="right")

        self.save_btn = ctk.CTkButton(
            self.action_frame, text="Save", width=80, height=35,
            command=self.save_note, font=ctk.CTkFont(family="Inter", size=13, weight="bold"),
            fg_color=("#3b82f6", "#2563eb"), hover_color=("#2563eb", "#1d4ed8"),
            corner_radius=8
        )
        self.save_btn.pack(side="left", padx=5)

        self.delete_btn = ctk.CTkButton(
            self.action_frame, text="Delete", width=80, height=35,
            fg_color=("#ef4444", "#dc2626"), hover_color=("#dc2626", "#b91c1c"), 
            command=self.delete_note, font=ctk.CTkFont(family="Inter", size=13, weight="bold"),
            corner_radius=8
        )
        self.delete_btn.pack(side="left", padx=5)

        # Editor
        self.textbox = ctk.CTkTextbox(
            self.editor_frame, 
            wrap="word", 
            font=ctk.CTkFont(family="Inter", size=16),
            border_width=0,
            fg_color=("white", "#1e1e1e"),
            text_color=("black", "#e0e0e0"),
            corner_radius=12,
            undo=True # Enable undo/redo
        )
        self.textbox.grid(row=1, column=0, sticky="nsew", padx=30, pady=(0, 20))
        self.textbox.bind("<KeyRelease>", self._on_key_release)
        
        # Shortcuts for Undo/Redo
        self.textbox.bind("<Control-z>", lambda e: self._on_undo())
        self.textbox.bind("<Control-y>", lambda e: self._on_redo())
        self.textbox.bind("<Control-S>", lambda e: self._on_manual_save())
        self.textbox.bind("<Control-s>", lambda e: self._on_manual_save())

        # Bottom Bar (AI Features & Progress)
        self.bottom_frame = ctk.CTkFrame(self.editor_frame, fg_color="transparent")
        self.bottom_frame.grid(row=2, column=0, sticky="ew", padx=30, pady=(0, 30))

        # Progress container (fixed height) to prevent UI jumping
        self.progress_container = ctk.CTkFrame(self.bottom_frame, height=14, fg_color="transparent")
        self.progress_container.pack(fill="x", pady=(0, 10))
        self.progress_container.pack_propagate(False)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_container, mode="indeterminate", height=6,
            progress_color=("#3b82f6", "#2563eb"),
            fg_color=("gray90", "#2d2d2d")
        )
        self.progress_bar.set(0)

        self.ai_bar = ctk.CTkFrame(self.bottom_frame, height=60, fg_color=("#f3f4f6", "#1e1e1e"), corner_radius=12)
        self.ai_bar.pack(fill="x")

        self.ai_tools_label = ctk.CTkLabel(
            self.ai_bar, text="  ✨ AI TOOLS  ", 
            font=ctk.CTkFont(family="Inter", size=11, weight="bold"), 
            text_color=("gray40", "gray50")
        )
        self.ai_tools_label.pack(side="left", padx=(15, 5))

        ai_btn_style = {
            "font": ctk.CTkFont(family="Inter", size=12, weight="normal"),
            "height": 32,
            "corner_radius": 6,
            "fg_color": ("white", "#2d2d2d"),
            "text_color": ("gray10", "gray90"),
            "hover_color": ("gray90", "#3d3d3d"),
            "border_width": 1,
            "border_color": ("gray85", "#3d3d3d")
        }

        self.sum_btn = ctk.CTkButton(self.ai_bar, text="Summarize", width=90, command=lambda: self.run_ai("summarize"), **ai_btn_style)
        self.sum_btn.pack(side="left", padx=5)

        self.title_gen_btn = ctk.CTkButton(self.ai_bar, text="Gen Title", width=90, command=lambda: self.run_ai("title"), **ai_btn_style)
        self.title_gen_btn.pack(side="left", padx=5)
        
        self.explain_btn = ctk.CTkButton(self.ai_bar, text="Explain", width=80, command=lambda: self.run_ai("explain"), **ai_btn_style)
        self.explain_btn.pack(side="left", padx=5)

        self.questions_btn = ctk.CTkButton(self.ai_bar, text="Study Qs", width=80, command=lambda: self.run_ai("questions"), **ai_btn_style)
        self.questions_btn.pack(side="left", padx=5)

        self.export_btn = ctk.CTkButton(
            self.ai_bar, text="Export TXT", width=100, 
            fg_color="transparent", hover_color=("gray90", "#3d3d3d"), 
            text_color=("gray10", "gray90"),
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            command=self.export_note
        )
        self.export_btn.pack(side="right", padx=(5, 15))

        self.status_label = ctk.CTkLabel(self.ai_bar, text="", text_color=("gray40", "gray50"), font=ctk.CTkFont(family="Inter", size=11))
        self.status_label.pack(side="right", padx=10)

    def load_notes(self, query=""):
        for widget in self.scrollable_list.winfo_children():
            widget.destroy()

        notes = NoteService.search_notes(query) if query else NoteService.get_all_notes()
        
        for note in notes:
            # Custom styled button for notes list
            title_text = note.title if note.title.strip() else "Untitled Note"
            if len(title_text) > 22:
                title_text = title_text[:19] + "..."
            
            # Highlight current note
            is_current = self.current_note and self.current_note.id == note.id
            bg_color = ("#e5e7eb", "#2563eb") if is_current else "transparent"
            text_color = ("#111827", "white") if is_current else ("gray10", "gray70")
            border_color = ("#d1d5db", "#2d2d2d") if not is_current else ("#3b82f6", "#2563eb")

            btn = ctk.CTkButton(
                self.scrollable_list, 
                text=title_text, 
                font=ctk.CTkFont(family="Inter", size=14, weight="normal"),
                fg_color=bg_color,
                text_color=text_color, 
                hover_color=("#f3f4f6", "#2d2d2d") if not is_current else ("#2563eb", "#1d4ed8"),
                border_width=1 if not is_current else 0,
                border_color=border_color,
                anchor="w",
                height=45,
                corner_radius=10,
                command=lambda n=note: self.open_note(n)
            )
            btn.pack(fill="x", pady=2, padx=10)

    def on_search(self, event):
        query = self.search_entry.get()
        self.load_notes(query)

    def create_new_note(self):
        self.current_note = None
        self.title_entry.delete(0, "end")
        self.textbox.delete("1.0", "end")
        self.textbox.edit_reset() # Clear undo stack
        self.status_label.configure(text="New note created.")

    def open_note(self, note):
        self.current_note = note
        self.title_entry.delete(0, "end")
        self.title_entry.insert(0, note.title)
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", note.content)
        self.textbox.edit_reset() # Clear undo stack
        self.status_label.configure(text=f"Last updated: {note.updated_at[:16].replace('T', ' ')}")
        self.load_notes(self.search_entry.get()) # Refresh list to update highlight

    def _on_key_release(self, event=None):
        self._schedule_save()
        
        # Insert undo separator on word boundaries or sentences
        if event and event.keysym in ("space", "Return", "period", "exclam", "question"):
            try:
                self.textbox.edit_separator()
            except:
                pass

    def _schedule_save(self, event=None):
        if self._save_timer is not None:
            self.after_cancel(self._save_timer)
        self.status_label.configure(text="Unsaved changes...")
        self._save_timer = self.after(1500, self.save_note)

    def save_note(self):
        title = self.title_entry.get().strip() or "Untitled"
        content = self.textbox.get("1.0", "end-1c")
        
        if not title.strip() and not content.strip():
            return

        if self.current_note:
            NoteService.update_note(self.current_note.id, title, content)
            self.current_note.title = title
            self.current_note.content = content
            self.status_label.configure(text="Auto-saved.")
        else:
            self.current_note = NoteService.create_note(title, content)
            self.status_label.configure(text="Note created.")
            
        self.load_notes(self.search_entry.get())

    def delete_note(self):
        if self.current_note:
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this note?"):
                NoteService.delete_note(self.current_note.id)
                self.create_new_note()
                self.load_notes()
                self.status_label.configure(text="Note deleted.")

    def export_note(self):
        if self.current_note:
            self.save_note()
            try:
                path = ExportService.export_to_txt(self.current_note)
                self.status_label.configure(text=f"Exported to exports/")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))
        else:
            messagebox.showinfo("Export", "No note to export.")

    def _set_ai_state(self, is_running):
        state = "disabled" if is_running else "normal"
        self.sum_btn.configure(state=state)
        self.title_gen_btn.configure(state=state)
        self.explain_btn.configure(state=state)
        self.questions_btn.configure(state=state)
        
        if is_running:
            self.progress_bar.pack(fill="x", side="bottom")
            self.progress_bar.start()
            self.status_label.configure(text="AI is thinking...")
        else:
            self.progress_bar.stop()
            self.progress_bar.pack_forget()

    def run_ai(self, action):
        content = self.textbox.get("1.0", "end-1c").strip()
        if not content:
            messagebox.showwarning("Empty Note", "Please write some content first.")
            return

        self._set_ai_state(True)
        self.update_idletasks()

        def ai_task():
            try:
                res = ""
                modal_title = "AI Preview"
                if action == "summarize":
                    res = AIService.summarize_note(content)
                    modal_title = "Summary Preview"
                elif action == "title":
                    res = AIService.generate_title(content)
                    modal_title = "Title Preview"
                elif action == "explain":
                    res = AIService.explain_note(content)
                    modal_title = "Explanation Preview"
                elif action == "questions":
                    res = AIService.generate_study_questions(content)
                    modal_title = "Study Questions Preview"
                
                self.after(0, lambda: self.status_label.configure(text="AI task completed."))
                self.after(0, lambda: self.show_ai_preview_modal(modal_title, res, action))
            except Exception as e:
                err_msg = str(e)
                self.after(0, lambda: self.status_label.configure(text="AI task failed."))
                self.after(0, lambda msg=err_msg: messagebox.showerror("AI Error", msg))
            finally:
                self.after(0, lambda: self._set_ai_state(False))

        threading.Thread(target=ai_task, daemon=True).start()

    def show_ai_preview_modal(self, title: str, ai_text: str, action: str):
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("600x450")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        dialog.grid_rowconfigure(0, weight=1)
        dialog.grid_columnconfigure(0, weight=1)

        # Main frame
        main_frame = ctk.CTkFrame(dialog, fg_color=("gray95", "gray13"))
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        header = ctk.CTkLabel(main_frame, text="AI Generated Result", font=ctk.CTkFont(size=18, weight="bold"))
        header.grid(row=0, column=0, pady=(10, 10), sticky="w", padx=20)

        # Textbox
        tb = ctk.CTkTextbox(
            main_frame, 
            wrap="word", 
            font=ctk.CTkFont(size=15),
            fg_color=("white", "gray20"),
            text_color=("black", "white"),
            border_width=1,
            border_color=("gray80", "gray30")
        )
        tb.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        tb.insert("1.0", ai_text)
        tb.configure(state="disabled") # Read only

        # Button frame
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.grid(row=2, column=0, sticky="e", padx=20, pady=(10, 20))

        def on_apply():
            if action == "title":
                self._update_title(ai_text)
            else:
                section_header = f"\n\n--- AI {title.replace(' Preview', '')} ---\n"
                self._append_to_editor(section_header + ai_text)
            dialog.destroy()

        def on_discard():
            dialog.destroy()

        discard_btn = ctk.CTkButton(
            btn_frame, text="Discard", width=80, 
            fg_color=("#e74c3c", "#c0392b"), hover_color=("#c0392b", "#e74c3c"),
            command=on_discard
        )
        discard_btn.pack(side="right", padx=(10, 0))

        apply_btn = ctk.CTkButton(
            btn_frame, text="Apply to Note", width=120,
            fg_color=("#2ecc71", "#27ae60"), hover_color=("#27ae60", "#2ecc71"),
            command=on_apply
        )
        apply_btn.pack(side="right")

    def _append_to_editor(self, text):
        self.textbox.insert("end", text)
        self.save_note()

    def _update_title(self, text):
        self.title_entry.delete(0, "end")
        self.title_entry.insert(0, text)
        self.save_note()

    def _on_undo(self):
        try:
            self.textbox.edit_undo()
        except:
            pass
        return "break"

    def _on_redo(self):
        try:
            self.textbox.edit_redo()
        except:
            pass
        return "break"

    def _on_manual_save(self):
        self.save_note()
        return "break"
