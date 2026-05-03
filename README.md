# AI Notes App

A modern, production-style desktop notes application with AI-powered summarization, built using Python and CustomTkinter.

## Screenshots
*(Add screenshots here)*

## Features

* **Notes Management**: Create, edit, delete, search, and tag notes with auto-save support.
* **AI Integration**: Use OpenRouter API to summarize notes, generate titles, and explain content.
* **Modern UI**: Dark mode, responsive design, sidebar navigation, and loading states.
* **Data Storage**: Local SQLite database for fast and reliable storage.
* **Exports**: Export your notes to simple `.txt` files.

## Architecture

The project follows a clean, modular architecture separating UI, business logic, and database layers:

```
project/
├── app.py                     # Entry point
├── config/                    # Global configurations
├── database/                  # SQLite DB setup and schema
├── models/                    # Data representations
├── services/                  # Business logic (AI, Notes, Exports)
├── ui/                        # CustomTkinter frontend
├── utils/                     # Helpers, validators, logging
└── assets/                    # Static assets
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd ai-notes-app
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup:**
   * Copy the `.env.example` file to `.env`.
   * Open `.env` and add your OpenRouter API key.
   ```bash
   cp .env.example .env
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```
