import os
from datetime import datetime
from config.settings import EXPORTS_DIR
from models.note_model import Note
from utils.logger import setup_logger

logger = setup_logger("ExportService")

class ExportService:
    @staticmethod
    def export_to_txt(note: Note) -> str:
        """Exports a note to a text file in the exports directory."""
        try:
            safe_title = "".join([c for c in note.title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
            if not safe_title:
                safe_title = "Untitled"
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_title.replace(' ', '_')}_{timestamp}.txt"
            filepath = EXPORTS_DIR / filename
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"Title: {note.title}\n")
                f.write(f"Created: {note.created_at}\n")
                f.write(f"Updated: {note.updated_at}\n")
                f.write("-" * 40 + "\n\n")
                f.write(note.content)
                
            logger.info(f"Note exported to {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Failed to export note: {e}")
            raise
