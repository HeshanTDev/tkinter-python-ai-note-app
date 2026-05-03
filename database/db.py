import sqlite3
from config.settings import DB_PATH
from database.schema import SCHEMA_SQL
from utils.logger import setup_logger

logger = setup_logger("Database")

class Database:
    def __init__(self, db_path: str = str(DB_PATH)):
        self.db_path = db_path
        self._init_db()

    def get_connection(self) -> sqlite3.Connection:
        """Returns a new connection to the database."""
        conn = sqlite3.connect(self.db_path)
        # Enable foreign keys
        conn.execute("PRAGMA foreign_keys = 1")
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Initializes the database schema if it doesn't exist."""
        try:
            with self.get_connection() as conn:
                conn.executescript(SCHEMA_SQL)
                logger.info("Database initialized successfully.")
        except sqlite3.Error as e:
            logger.error(f"Error initializing database: {e}")
            raise

db = Database()
