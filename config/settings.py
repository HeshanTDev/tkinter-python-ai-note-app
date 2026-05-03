import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "database"
EXPORTS_DIR = BASE_DIR / "exports"

# Database Configuration
DB_NAME = "notes.db"
DB_PATH = DB_DIR / DB_NAME

# UI Configuration
WINDOW_TITLE = "AI Notes App"
WINDOW_SIZE = "1100x750"
THEME_COLOR = "blue"  # Updated to blue for a cleaner look
APPEARANCE_MODE = "dark"

# OpenRouter API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3-haiku")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Create necessary directories
DB_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
