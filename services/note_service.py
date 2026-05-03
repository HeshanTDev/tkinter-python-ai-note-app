from typing import List, Optional
from datetime import datetime
from database.db import db
from models.note_model import Note, Tag
from utils.logger import setup_logger

logger = setup_logger("NoteService")

class NoteService:
    @staticmethod
    def _get_current_time() -> str:
        return datetime.now().isoformat()

    @staticmethod
    def create_note(title: str, content: str) -> Note:
        now = NoteService._get_current_time()
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO notes (title, content, created_at, updated_at) VALUES (?, ?, ?, ?)",
                    (title, content, now, now)
                )
                note_id = cursor.lastrowid
                return Note(id=note_id, title=title, content=content, created_at=now, updated_at=now)
        except Exception as e:
            logger.error(f"Failed to create note: {e}")
            raise

    @staticmethod
    def update_note(note_id: int, title: str, content: str) -> None:
        now = NoteService._get_current_time()
        try:
            with db.get_connection() as conn:
                conn.execute(
                    "UPDATE notes SET title = ?, content = ?, updated_at = ? WHERE id = ?",
                    (title, content, now, note_id)
                )
        except Exception as e:
            logger.error(f"Failed to update note {note_id}: {e}")
            raise

    @staticmethod
    def delete_note(note_id: int) -> None:
        try:
            with db.get_connection() as conn:
                conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        except Exception as e:
            logger.error(f"Failed to delete note {note_id}: {e}")
            raise

    @staticmethod
    def get_all_notes() -> List[Note]:
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM notes ORDER BY updated_at DESC")
                rows = cursor.fetchall()
                notes = []
                for row in rows:
                    notes.append(Note(
                        id=row['id'],
                        title=row['title'],
                        content=row['content'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    ))
                return notes
        except Exception as e:
            logger.error(f"Failed to get notes: {e}")
            return []

    @staticmethod
    def search_notes(query: str) -> List[Note]:
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                search_query = f"%{query}%"
                cursor.execute(
                    "SELECT * FROM notes WHERE title LIKE ? OR content LIKE ? ORDER BY updated_at DESC",
                    (search_query, search_query)
                )
                rows = cursor.fetchall()
                notes = []
                for row in rows:
                    notes.append(Note(
                        id=row['id'],
                        title=row['title'],
                        content=row['content'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    ))
                return notes
        except Exception as e:
            logger.error(f"Failed to search notes: {e}")
            return []
