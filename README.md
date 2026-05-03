# AI Notes App

A modern, professional desktop note-taking application with AI-powered tools. Built with Python, CustomTkinter, and OpenRouter API.

## ✨ Features

- **Create, Edit & Delete Notes** — Full CRUD with auto-save
- **Smart Search** — Real-time search with debounced input
- **AI Tools Dashboard** — Summarize, simplify, explain, generate study questions & titles
- **Export** — Save notes as `.txt` files
- **Dark/Light/System Theme** — Toggle appearance modes
- **Settings Panel** — Configure API key and model from within the app
- **Keyboard Shortcuts** — Ctrl+S (save), Ctrl+Z (undo), Ctrl+Y (redo)
- **Word Count** — Live word and character count in the editor footer

## 🏗 Architecture

```
project/
├── app.py                    # Entry point
├── config/
│   ├── settings.py           # App configuration
│   └── theme.py              # Design tokens (colors, fonts, spacing)
├── database/
│   ├── db.py                 # SQLite connection manager
│   └── schema.py             # Table definitions
├── models/
│   └── note_model.py         # Data models (Note, Tag)
├── repositories/
│   └── note_repository.py    # Raw database CRUD
├── services/
│   ├── ai_service.py         # OpenRouter AI integration
│   ├── note_service.py       # Business logic layer
│   └── export_service.py     # TXT export
├── ui/
│   ├── main_window.py        # Root window + page routing
│   ├── sidebar.py            # Navigation sidebar
│   ├── notes_page.py         # Notes list + editor
│   ├── ai_tools_page.py      # AI tools dashboard
│   ├── settings_page.py      # Settings panel
│   └── components/
│       ├── note_card.py       # Reusable note list card
│       ├── search_bar.py      # Reusable search widget
│       └── modal.py           # Reusable modal dialog
├── utils/
│   └── logger.py             # Centralized logging
├── assets/
└── exports/                  # Exported note files
```

### Design Principles

- **Repository Pattern** — SQL isolated in `repositories/`, services never touch the DB directly
- **Component-Based UI** — Reusable widgets in `ui/components/`
- **Design Token System** — All colors, fonts, and spacing centralized in `config/theme.py`
- **Separation of Concerns** — UI, business logic, and data access are strictly separated

## 🚀 Installation

### Prerequisites

- Python 3.10+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-notes-app.git
cd ai-notes-app

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OpenRouter API key
```

### Environment Variables

| Variable | Description | Default |
|---|---|---|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | (required for AI features) |
| `OPENROUTER_MODEL` | AI model to use | `anthropic/claude-3-haiku` |

## ▶️ Running

```bash
python app.py
```

## 📦 Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core language |
| CustomTkinter | Modern UI framework |
| SQLite | Local database |
| OpenRouter API | AI features |
| python-dotenv | Environment management |

## 🔮 Future Improvements

- [ ] Markdown rendering in the editor
- [ ] Note tagging and filtering
- [ ] Note pinning and favorites
- [ ] Rich text formatting toolbar
- [ ] PDF export support
- [ ] Cloud sync
- [ ] Multi-language support

## 📄 License

MIT License
