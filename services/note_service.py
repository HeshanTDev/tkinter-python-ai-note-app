"""
services/note_service.py
Business-level operations for notes.
Delegates all database work to NoteRepository.
"""

from typing import List
from datetime import datetime
from models.note_model import Note
from repositories.note_repository import NoteRepository
from utils.logger import setup_logger

logger = setup_logger("NoteService")


class NoteService:
    """High-level note operations — auto-timestamps, validation, etc."""

    @staticmethod
    def create_note(title: str, content: str) -> Note:
        """Create a new note with automatic timestamps."""
        now = datetime.now().isoformat()
        note_id = NoteRepository.insert(title, content, now, now)
        logger.info(f"Created note id={note_id}")
        return Note(id=note_id, title=title, content=content, created_at=now, updated_at=now)

    @staticmethod
    def update_note(note_id: int, title: str, content: str) -> None:
        """Update an existing note (auto-refreshes updated_at)."""
        now = datetime.now().isoformat()
        NoteRepository.update(note_id, title, content, now)

    @staticmethod
    def delete_note(note_id: int) -> None:
        """Delete a note by id."""
        NoteRepository.delete(note_id)
        logger.info(f"Deleted note id={note_id}")

    @staticmethod
    def get_all_notes() -> List[Note]:
        """Return all notes, newest first."""
        return NoteRepository.fetch_all()

    @staticmethod
    def search_notes(query: str) -> List[Note]:
        """Search notes by title or content."""
        return NoteRepository.search(query)

    @staticmethod
    def get_note_count() -> int:
        """Return total number of notes."""
        return NoteRepository.get_count()
