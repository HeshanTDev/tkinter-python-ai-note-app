from models.note_model import Note
from utils.logger import setup_logger

logger = setup_logger("ExportService")

class ExportService:
    @staticmethod
    def export_to_txt(note: Note, filepath: str) -> str:
        """Exports a note to a specified text file path."""
        try:
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
