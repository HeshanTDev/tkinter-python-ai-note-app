"""
ui/notes_page.py
Main notes page — split into a list pane (left) and editor pane (right).
Uses reusable NoteCard, SearchBar, and Modal components.
"""

import customtkinter as ctk
import threading
from tkinter import messagebox, filedialog
from typing import Optional

from config.theme import COLORS, FONTS, RADIUS, SPACING
from models.note_model import Note
from services.note_service import NoteService
from services.export_service import ExportService
from ui.components.note_card import NoteCard
from ui.components.search_bar import SearchBar
from ui.components.modal import Modal


class NotesPage(ctk.CTkFrame):
    """The primary page — note list on the left, editor on the right."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.grid_columnconfigure(0, weight=0, minsize=300)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.current_note: Optional[Note] = None
        self._ai_running = False

        self._create_list_pane()
        self._create_editor_pane()
        self.load_notes()

    # ═══════════════════════════════════════════════════════════════════════
    #  LIST PANE (left column)
    # ═══════════════════════════════════════════════════════════════════════

    def _create_list_pane(self):
        """Build the left sidebar: search bar, new-note button, scrollable list."""
        self.list_frame = ctk.CTkFrame(
            self, width=300, corner_radius=0,
            fg_color=COLORS["bg_list"],
            border_width=1, border_color=COLORS["border"],
        )
        self.list_frame.grid(row=0, column=0, sticky="nsew")
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_rowconfigure(2, weight=1)
        self.list_frame.grid_propagate(False)

        # ── Header section ───────────────────────────────────────────────────
        header = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=16, pady=(20, 0))
        header.grid_columnconfigure(0, weight=1)

        # Notes title + count badge
        title_row = ctk.CTkFrame(header, fg_color="transparent")
        title_row.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            title_row,
            text="Notes",
            font=ctk.CTkFont(family=FONTS["h2"][0], size=FONTS["h2"][1], weight="bold"),
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        self.count_label = ctk.CTkLabel(
            title_row,
            text="0",
            font=ctk.CTkFont(family=FONTS["caption"][0], size=10, weight="bold"),
            text_color=COLORS["text_white"],
            fg_color=(COLORS["accent"], COLORS["accent"]),
            corner_radius=10,
            width=28, height=20,
        )
        self.count_label.pack(side="left", padx=(8, 0))

        # Search bar
        self.search_bar = SearchBar(header, on_search=self._on_search)
        self.search_bar.pack(fill="x", pady=(0, 10))

        # New note button
        self.new_btn = ctk.CTkButton(
            header,
            text="+   New Note",
            command=self.create_new_note,
            font=ctk.CTkFont(family=FONTS["body"][0], size=FONTS["body"][1], weight="bold"),
            height=42,
            corner_radius=RADIUS["md"],
            fg_color=(COLORS["accent"], COLORS["accent"]),
            hover_color=(COLORS["accent_hover"], COLORS["accent_hover"]),
            text_color=COLORS["text_white"],
        )
        self.new_btn.pack(fill="x")

        # ── Scrollable note list ─────────────────────────────────────────────
        self.scrollable_list = ctk.CTkScrollableFrame(
            self.list_frame, fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
        )
        self.scrollable_list.grid(row=2, column=0, sticky="nsew", padx=8, pady=(12, 8))
        self.scrollable_list.grid_columnconfigure(0, weight=1)

        # ── Empty state ──────────────────────────────────────────────────────
        self.empty_state = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        self.empty_label = ctk.CTkLabel(
            self.empty_state,
            text="📄\n\nNo notes yet.\nClick '+ New Note' to start.",
            font=ctk.CTkFont(family=FONTS["body"][0], size=FONTS["body"][1]),
            text_color=COLORS["text_muted"],
            justify="center",
        )
        self.empty_label.pack(expand=True)

    # ═══════════════════════════════════════════════════════════════════════
    #  EDITOR PANE (right column)
    # ═══════════════════════════════════════════════════════════════════════

    def _create_editor_pane(self):
        """Build the right editor: title bar, textbox, status/AI footer."""
        self.editor_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color=COLORS["bg_editor"],
        )
        self.editor_frame.grid(row=0, column=1, sticky="nsew")
        self.editor_frame.grid_columnconfigure(0, weight=1)
        self.editor_frame.grid_rowconfigure(1, weight=1)

        # ── Top bar (title + action buttons) ─────────────────────────────────
        top_bar = ctk.CTkFrame(self.editor_frame, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=SPACING["xl"], pady=(SPACING["lg"], SPACING["sm"]))

        self.title_entry = ctk.CTkEntry(
            top_bar,
            placeholder_text="Untitled Note",
            font=ctk.CTkFont(family=FONTS["h1"][0], size=FONTS["h1"][1], weight="bold"),
            border_width=0,
            fg_color="transparent",
            text_color=COLORS["text_primary"],
            height=48,
        )
        self.title_entry.pack(side="left", fill="x", expand=True, padx=(0, 16))
        self.title_entry.bind("<KeyRelease>", self._on_title_key)

        # Action buttons frame
        actions = ctk.CTkFrame(top_bar, fg_color="transparent")
        actions.pack(side="right")

        self.save_btn = ctk.CTkButton(
            actions, text="💾  Save", width=90, height=36,
            command=self.save_note,
            font=ctk.CTkFont(family=FONTS["body_sm"][0], size=FONTS["body_sm"][1], weight="bold"),
            fg_color=(COLORS["accent"], COLORS["accent"]),
            hover_color=(COLORS["accent_hover"], COLORS["accent_hover"]),
            corner_radius=RADIUS["sm"],
        )
        self.save_btn.pack(side="left", padx=4)

        self.export_btn = ctk.CTkButton(
            actions, text="📤  Export", width=90, height=36,
            command=self.export_note,
            font=ctk.CTkFont(family=FONTS["body_sm"][0], size=FONTS["body_sm"][1], weight="bold"),
            fg_color="transparent",
            hover_color=COLORS["hover_card"],
            text_color=COLORS["text_secondary"],
            border_width=1, border_color=COLORS["border"],
            corner_radius=RADIUS["sm"],
        )
        self.export_btn.pack(side="left", padx=4)

        self.delete_btn = ctk.CTkButton(
            actions, text="🗑  Delete", width=90, height=36,
            command=self.delete_note,
            font=ctk.CTkFont(family=FONTS["body_sm"][0], size=FONTS["body_sm"][1], weight="bold"),
            fg_color=(COLORS["danger"], COLORS["danger"]),
            hover_color=(COLORS["danger_hover"], COLORS["danger_hover"]),
            text_color=COLORS["text_white"],
            corner_radius=RADIUS["sm"],
        )
        self.delete_btn.pack(side="left", padx=4)

        # ── Editor textbox ───────────────────────────────────────────────────
        self.textbox = ctk.CTkTextbox(
            self.editor_frame,
            wrap="word",
            font=ctk.CTkFont(family=FONTS["body_lg"][0], size=FONTS["body_lg"][1]),
            border_width=0,
            fg_color=COLORS["bg_input"],
            text_color=COLORS["text_primary"],
            corner_radius=RADIUS["lg"],
            undo=True,
        )
        self.textbox.grid(row=1, column=0, sticky="nsew", padx=SPACING["xl"], pady=(4, 8))
        self.textbox.bind("<KeyRelease>", self._on_key_release)

        # Keyboard shortcuts
        self.textbox.bind("<Control-z>", lambda e: self._on_undo())
        self.textbox.bind("<Control-y>", lambda e: self._on_redo())
        self.textbox.bind("<Control-s>", lambda e: self._on_manual_save())
        self.textbox.bind("<Control-S>", lambda e: self._on_manual_save())

        # ── Footer bar (status + word count + progress) ──────────────────────
        self.footer = ctk.CTkFrame(self.editor_frame, fg_color="transparent", height=36)
        self.footer.grid(row=2, column=0, sticky="ew", padx=SPACING["xl"], pady=(0, 12))
        self.footer.grid_propagate(False)

        self.status_label = ctk.CTkLabel(
            self.footer,
            text="Ready",
            font=ctk.CTkFont(family=FONTS["caption"][0], size=FONTS["caption"][1]),
            text_color=COLORS["text_muted"],
            anchor="w",
        )
        self.status_label.pack(side="left")

        self.word_count_label = ctk.CTkLabel(
            self.footer,
            text="0 words",
            font=ctk.CTkFont(family=FONTS["caption"][0], size=FONTS["caption"][1]),
            text_color=COLORS["text_muted"],
            anchor="e",
        )
        self.word_count_label.pack(side="right")

        # Progress bar (hidden by default)
        self.progress_bar = ctk.CTkProgressBar(
            self.footer, mode="indeterminate", height=4, width=120,
            progress_color=(COLORS["accent"], COLORS["accent"]),
            fg_color=COLORS["border"],
        )

    # ═══════════════════════════════════════════════════════════════════════
    #  NOTE LIST OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════

    def load_notes(self, query: str = ""):
        """Reload the note list from the database."""
        for widget in self.scrollable_list.winfo_children():
            widget.destroy()

        notes = NoteService.search_notes(query) if query else NoteService.get_all_notes()
        count = len(notes)

        # Update badge
        self.count_label.configure(text=str(count))

        # Show empty state or list
        if count == 0:
            self.scrollable_list.grid_forget()
            self.empty_state.grid(row=2, column=0, sticky="nsew", padx=8, pady=12)
        else:
            self.empty_state.grid_forget()
            self.scrollable_list.grid(row=2, column=0, sticky="nsew", padx=8, pady=(12, 8))

            for note in notes:
                is_active = self.current_note and self.current_note.id == note.id
                card = NoteCard(
                    self.scrollable_list,
                    title=note.title,
                    content=note.content,
                    timestamp=note.updated_at,
                    is_active=is_active,
                    on_click=lambda n=note: self.open_note(n),
                )
                card.pack(fill="x", pady=3)

    def _on_search(self, query: str):
        """Called by the SearchBar component."""
        self.load_notes(query)

    # ═══════════════════════════════════════════════════════════════════════
    #  NOTE CRUD
    # ═══════════════════════════════════════════════════════════════════════

    def create_new_note(self):
        """Clear the editor for a brand-new note."""
        self.current_note = None
        self.search_bar.clear()
        self.title_entry.delete(0, "end")
        self.textbox.delete("1.0", "end")
        try:
            self.textbox.edit_reset()
        except Exception:
            pass
        self._update_status("New note — start typing!")
        self._update_word_count()
        self.title_entry.focus_set()
        self.load_notes()

    def open_note(self, note: Note):
        """Load a note into the editor."""
        self.current_note = note
        self.title_entry.delete(0, "end")
        self.title_entry.insert(0, note.title)
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", note.content)
        try:
            self.textbox.edit_reset()
        except Exception:
            pass
        self._update_status(f"Opened • {self._format_time(note.updated_at)}")
        self._update_word_count()
        self.load_notes(self.search_bar.get())

    def save_note(self):
        """Save the current note (create or update)."""
        title = self.title_entry.get().strip() or "Untitled"
        content = self.textbox.get("1.0", "end-1c")

        if not title and not content.strip():
            return

        if self.current_note:
            NoteService.update_note(self.current_note.id, title, content)
            self.current_note.title = title
            self.current_note.content = content
            self._update_status("Saved ✓")
        else:
            self.current_note = NoteService.create_note(title, content)
            self._update_status("Created ✓")

        self.load_notes(self.search_bar.get())

    def delete_note(self):
        """Delete the current note with confirmation."""
        if not self.current_note:
            return
        if messagebox.askyesno("Delete Note", "Are you sure you want to delete this note?"):
            NoteService.delete_note(self.current_note.id)
            self.create_new_note()
            self._update_status("Note deleted.")

    def export_note(self):
        """Export the current note to a .txt file with a file selection dialog."""
        if not self.current_note:
            messagebox.showinfo("Export", "Save a note first before exporting.")
            return

        # Prepare default filename
        safe_title = "".join([c for c in self.current_note.title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        if not safe_title:
            safe_title = "Untitled"
        default_filename = f"{safe_title.replace(' ', '_')}.txt"

        # Open file dialog
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=default_filename,
            title="Export Note"
        )

        if not filepath:
            return  # User cancelled

        self.save_note()
        try:
            ExportService.export_to_txt(self.current_note, filepath)
            self._update_status(f"Exported to {filepath} ✓")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    # ═══════════════════════════════════════════════════════════════════════
    #  AI FEATURES
    # ═══════════════════════════════════════════════════════════════════════

    def run_ai(self, action: str):
        """Run an AI action on the current note content."""
        content = self.textbox.get("1.0", "end-1c").strip()
        if not content:
            messagebox.showwarning("Empty Note", "Write some content first.")
            return
        if self._ai_running:
            return  # Prevent duplicate requests

        self._set_ai_loading(True)

        def task():
            try:
                from services.ai_service import AIService
                result = ""
                modal_title = "AI Result"

                if action == "summarize":
                    result = AIService.summarize_note(content)
                    modal_title = "📋  Summary"
                elif action == "title":
                    result = AIService.generate_title(content)
                    modal_title = "✏️  Generated Title"
                elif action == "explain":
                    result = AIService.explain_note(content)
                    modal_title = "💡  Explanation"
                elif action == "questions":
                    result = AIService.generate_study_questions(content)
                    modal_title = "❓  Study Questions"
                elif action == "simplify":
                    result = AIService.simplify_note(content)
                    modal_title = "🔤  Simplified"

                self.after(0, lambda: self._show_ai_result(modal_title, result, action))
                self.after(0, lambda: self._update_status("AI completed ✓"))
            except Exception as e:
                err = str(e)
                self.after(0, lambda: messagebox.showerror("AI Error", err))
                self.after(0, lambda: self._update_status("AI failed."))
            finally:
                self.after(0, lambda: self._set_ai_loading(False))

        threading.Thread(target=task, daemon=True).start()

    def _show_ai_result(self, title: str, text: str, action: str):
        """Show AI result in a modal with Apply / Discard buttons."""
        modal = Modal(self, title=title)
        modal.set_body_text(text)

        def apply():
            if action == "title":
                self.title_entry.delete(0, "end")
                self.title_entry.insert(0, text.strip())
            else:
                # Add undo separator so Ctrl+Z undoes the entire AI block
                try:
                    self.textbox.edit_separator()
                except Exception:
                    pass
                section = f"\n\n--- {title.replace('  ', ' ').strip()} ---\n{text}"
                self.textbox.insert("end", section)
                try:
                    self.textbox.edit_separator()
                except Exception:
                    pass
            self._mark_unsaved()
            self._update_word_count()
            modal.destroy()

        modal.add_button("Discard", modal.destroy, style="danger")
        modal.add_button("Apply to Note", apply, style="primary")

    def _set_ai_loading(self, loading: bool):
        """Show/hide loading indicator and disable AI interactions."""
        self._ai_running = loading
        if loading:
            self.progress_bar.pack(side="left", padx=(12, 0))
            self.progress_bar.start()
            self._update_status("AI is thinking...")
        else:
            self.progress_bar.stop()
            self.progress_bar.pack_forget()

    # ═══════════════════════════════════════════════════════════════════════
    #  EDITOR HELPERS
    # ═══════════════════════════════════════════════════════════════════════

    def _on_key_release(self, event=None):
        """Handle keystrokes in the textbox — update word count + mark unsaved."""
        self._mark_unsaved()
        self._update_word_count()
        # Add undo separators on word boundaries
        if event and event.keysym in ("space", "Return", "period", "exclam", "question"):
            try:
                self.textbox.edit_separator()
            except Exception:
                pass

    def _on_title_key(self, event=None):
        """Handle keystrokes in the title — just mark unsaved."""
        self._mark_unsaved()

    def _mark_unsaved(self):
        """Show unsaved status indicator."""
        self._update_status("● Unsaved changes")

    def _update_status(self, text: str):
        self.status_label.configure(text=text)

    def _update_word_count(self):
        content = self.textbox.get("1.0", "end-1c").strip()
        words = len(content.split()) if content else 0
        chars = len(content)
        self.word_count_label.configure(text=f"{words} words  •  {chars} chars")

    def _on_undo(self):
        try:
            self.textbox.edit_undo()
        except Exception:
            pass
        return "break"

    def _on_redo(self):
        try:
            self.textbox.edit_redo()
        except Exception:
            pass
        return "break"

    def _on_manual_save(self):
        self.save_note()
        return "break"

    @staticmethod
    def _format_time(iso_str: str) -> str:
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(iso_str)
            return dt.strftime("%d %b %Y • %H:%M")
        except Exception:
            return iso_str[:16].replace("T", " ")
