"""
ui/ai_tools_page.py
Dedicated AI Tools page — a clean dashboard of all AI-powered actions.
Separated from notes_page to keep concerns isolated.
"""

import customtkinter as ctk
import threading
from tkinter import messagebox
from typing import Optional

from config.theme import COLORS, FONTS, RADIUS, SPACING
from services.ai_service import AIService
from services.note_service import NoteService
from ui.components.modal import Modal


class AIToolsPage(ctk.CTkFrame):
    """AI Tools dashboard — select a note and run AI operations on it."""

    AI_ACTIONS = [
        {"key": "summarize",  "label": "📋  Summarize",         "desc": "Get a concise summary of your note"},
        {"key": "simplify",   "label": "🔤  Simplify",          "desc": "Rewrite in simpler language"},
        {"key": "explain",    "label": "💡  Explain",            "desc": "Break down complex concepts"},
        {"key": "questions",  "label": "❓  Study Questions",    "desc": "Generate questions to test understanding"},
        {"key": "title",      "label": "✏️  Generate Title",     "desc": "Create a catchy title from content"},
    ]

    def __init__(self, master, get_notes_page=None, **kwargs):
        super().__init__(master, fg_color=COLORS["bg_editor"], **kwargs)
        self._get_notes_page = get_notes_page
        self._ai_running = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # ── Header ───────────────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=40, pady=(36, 8))

        ctk.CTkLabel(
            header,
            text="✨  AI Tools",
            font=ctk.CTkFont(family=FONTS["h1"][0], size=FONTS["h1"][1], weight="bold"),
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        # Status / progress
        self.status_frame = ctk.CTkFrame(header, fg_color="transparent")
        self.status_frame.pack(side="right")

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Select a tool below",
            font=ctk.CTkFont(family=FONTS["caption"][0], size=FONTS["caption"][1]),
            text_color=COLORS["text_muted"],
        )
        self.status_label.pack(side="left")

        self.progress_bar = ctk.CTkProgressBar(
            self.status_frame, mode="indeterminate", height=4, width=100,
            progress_color=(COLORS["accent"], COLORS["accent"]),
            fg_color=COLORS["border"],
        )

        # ── Subtitle ─────────────────────────────────────────────────────────
        ctk.CTkLabel(
            self,
            text="Use AI to enhance your notes. These tools work on the currently selected note in My Notes.",
            font=ctk.CTkFont(family=FONTS["body"][0], size=FONTS["body"][1]),
            text_color=COLORS["text_secondary"],
            anchor="w",
        ).grid(row=1, column=0, sticky="ew", padx=40, pady=(0, 24))

        # ── Tool cards grid ──────────────────────────────────────────────────
        cards_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        cards_frame.grid(row=2, column=0, sticky="nsew", padx=32, pady=(0, 32))
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)

        for i, action in enumerate(self.AI_ACTIONS):
            row = i // 2
            col = i % 2
            self._create_tool_card(cards_frame, action, row, col)

    def _create_tool_card(self, parent, action: dict, row: int, col: int):
        """Build a single AI tool card."""
        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_card"],
            corner_radius=RADIUS["lg"],
            border_width=1,
            border_color=COLORS["border"],
        )
        card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)
        card.grid_columnconfigure(0, weight=1)

        # Title
        ctk.CTkLabel(
            card,
            text=action["label"],
            font=ctk.CTkFont(family=FONTS["h3"][0], size=FONTS["h3"][1], weight="bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 4))

        # Description
        ctk.CTkLabel(
            card,
            text=action["desc"],
            font=ctk.CTkFont(family=FONTS["body_sm"][0], size=FONTS["body_sm"][1]),
            text_color=COLORS["text_muted"],
            anchor="w",
        ).grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 16))

        # Run button
        btn = ctk.CTkButton(
            card,
            text="Run →",
            width=100,
            height=34,
            corner_radius=RADIUS["sm"],
            font=ctk.CTkFont(family=FONTS["body_sm"][0], size=FONTS["body_sm"][1], weight="bold"),
            fg_color=(COLORS["accent"], COLORS["accent"]),
            hover_color=(COLORS["accent_hover"], COLORS["accent_hover"]),
            text_color=COLORS["text_white"],
            command=lambda k=action["key"]: self._run_tool(k),
        )
        btn.grid(row=2, column=0, sticky="w", padx=20, pady=(0, 20))

    def _run_tool(self, action_key: str):
        """Execute an AI tool on the currently selected note."""
        # Get content from the notes page
        notes_page = self._get_notes_page() if self._get_notes_page else None
        if not notes_page or not notes_page.current_note:
            messagebox.showinfo(
                "No Note Selected",
                "Please select a note in 'My Notes' first, then come back here."
            )
            return

        content = notes_page.current_note.content.strip()
        if not content:
            messagebox.showwarning("Empty Note", "The selected note has no content.")
            return

        if self._ai_running:
            return

        self._set_loading(True)

        def task():
            try:
                result = ""
                modal_title = "AI Result"

                if action_key == "summarize":
                    result = AIService.summarize_note(content)
                    modal_title = "📋  Summary"
                elif action_key == "simplify":
                    result = AIService.simplify_note(content)
                    modal_title = "🔤  Simplified"
                elif action_key == "explain":
                    result = AIService.explain_note(content)
                    modal_title = "💡  Explanation"
                elif action_key == "questions":
                    result = AIService.generate_study_questions(content)
                    modal_title = "❓  Study Questions"
                elif action_key == "title":
                    result = AIService.generate_title(content)
                    modal_title = "✏️  Generated Title"

                self.after(0, lambda: self._show_result(modal_title, result, action_key, notes_page))
                self.after(0, lambda: self.status_label.configure(text="Completed ✓"))
            except Exception as e:
                err = str(e)
                self.after(0, lambda: messagebox.showerror("AI Error", err))
                self.after(0, lambda: self.status_label.configure(text="Failed — check your API key"))
            finally:
                self.after(0, lambda: self._set_loading(False))

        threading.Thread(target=task, daemon=True).start()

    def _show_result(self, title: str, text: str, action: str, notes_page):
        """Show result in a modal with an option to apply to the note."""
        modal = Modal(self, title=title)
        modal.set_body_text(text)

        def apply():
            if action == "title":
                notes_page.title_entry.delete(0, "end")
                notes_page.title_entry.insert(0, text.strip())
            else:
                # Add undo separator so Ctrl+Z undoes the entire AI block
                try:
                    notes_page.textbox.edit_separator()
                except Exception:
                    pass
                section = f"\n\n--- {title.replace('  ', ' ').strip()} ---\n{text}"
                notes_page.textbox.insert("end", section)
                try:
                    notes_page.textbox.edit_separator()
                except Exception:
                    pass
            notes_page._mark_unsaved()
            notes_page._update_word_count()
            modal.destroy()

        modal.add_button("Discard", modal.destroy, style="danger")
        modal.add_button("Apply to Note", apply, style="primary")

    def _set_loading(self, loading: bool):
        self._ai_running = loading
        if loading:
            self.status_label.configure(text="AI is thinking...")
            self.progress_bar.pack(side="left", padx=(8, 0))
            self.progress_bar.start()
        else:
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
