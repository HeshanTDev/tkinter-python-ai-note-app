"""
repositories/note_repository.py
Raw database CRUD operations for notes.
All SQL lives here — services never touch the database directly.
"""

from typing import List, Optional
from database.db import db
from models.note_model import Note
from utils.logger import setup_logger

logger = setup_logger("NoteRepository")


class NoteRepository:
    """Handles all direct database interactions for notes."""

    @staticmethod
    def insert(title: str, content: str, created_at: str, updated_at: str) -> int:
        """Insert a new note row. Returns the new row id."""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO notes (title, content, created_at, updated_at) VALUES (?, ?, ?, ?)",
                    (title, content, created_at, updated_at),
                )
                return cursor.lastrowid
        except Exception as e:
            logger.error(f"insert failed: {e}")
            raise

    @staticmethod
    def update(note_id: int, title: str, content: str, updated_at: str) -> None:
        """Update an existing note by id."""
        try:
            with db.get_connection() as conn:
                conn.execute(
                    "UPDATE notes SET title = ?, content = ?, updated_at = ? WHERE id = ?",
                    (title, content, updated_at, note_id),
                )
        except Exception as e:
            logger.error(f"update failed for note {note_id}: {e}")
            raise

    @staticmethod
    def delete(note_id: int) -> None:
        """Delete a note by id."""
        try:
            with db.get_connection() as conn:
                conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        except Exception as e:
            logger.error(f"delete failed for note {note_id}: {e}")
            raise

    @staticmethod
    def fetch_all() -> List[Note]:
        """Return every note, newest-updated first."""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM notes ORDER BY updated_at DESC")
                return [NoteRepository._row_to_note(r) for r in cursor.fetchall()]
        except Exception as e:
            logger.error(f"fetch_all failed: {e}")
            return []

    @staticmethod
    def search(query: str) -> List[Note]:
        """Full-text search on title and content."""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                like = f"%{query}%"
                cursor.execute(
                    "SELECT * FROM notes WHERE title LIKE ? OR content LIKE ? ORDER BY updated_at DESC",
                    (like, like),
                )
                return [NoteRepository._row_to_note(r) for r in cursor.fetchall()]
        except Exception as e:
            logger.error(f"search failed: {e}")
            return []

    @staticmethod
    def get_count() -> int:
        """Return the total number of notes."""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM notes")
                return cursor.fetchone()[0]
        except Exception:
            return 0

    # ── private ──────────────────────────────────────────────────────────────

    @staticmethod
    def _row_to_note(row) -> Note:
        """Convert a sqlite3.Row into a Note dataclass."""
        return Note(
            id=row["id"],
            title=row["title"],
            content=row["content"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
