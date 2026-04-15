
# 📝 Flog (Blog-Flog)

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Django 6.0](https://img.shields.io/badge/django-6.0-green.svg)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/docker-containerized-blue)](https://www.docker.com/)
[![TailwindCSS](https://img.shields.io/badge/CSS-Tailwind-38B2AC)](https://tailwindcss.com/)

**Flogg** is a high-performance, containerized blogging platform engineered for developers. It bridges the gap between structured technical writing and AI-driven content transformation, featuring a Git-inspired CLI and a fully asynchronous backend.

---

## 🚀 AI-Storyteller Feature Demo

Experience how Gemini 2.0 transforms technical blogs into creative stories or simplified summaries in real-time.

[https://github.com/user-attachments/assets/YOUR_VIDEO_ID_HERE](https://github.com/abhimisraw/assets/)
> *If the video doesn't load, you can view the [Screen Recording here](./assets/Screen%20Recording%202026-04-15%20at%209.12.11 PM.mov)*

---

## ✨ Key Features

- **⚡ Asynchronous Core:** Built on **ASGI (Daphne)** with Django 6.0 for non-blocking AI API calls and background task processing.
- **🤖 AI Storyteller:** Integrated with **Google Gemini** to rewrite or analyze blogs in any context (Simplify, Story-mode, Technical Deep-dive).
- **🎨 Modern UI/UX:** Powered by **HTMX** for a "Single Page App" feel without the JavaScript bloat, styled with **DaisyUI & Tailwind CSS**.
- **🛠 Git-like CLI:** Custom management commands to handle your content repository like a pro.
- **📝 Markdown First:** Full support for GFM (GitHub Flavored Markdown) with safe rendering.

---

## 🏗 Architecture & Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **App Server** | Django 6.0 + Daphne | Handles Async Logic, WebSockets, and AI Polling |
| **Database** | PostgreSQL 16 | Persistent relational storage |
| **Reverse Proxy**| Nginx | SSL termination and static file serving |
| **Task Queue** | Asyncio + Daphne | In-memory background tasks for AI processing |

---

## 🛠 Installation & Setup

### Prerequisites
- Docker & Docker Compose
- Poetry (for local development only)

### 1. Clone & Enter
```bash
git clone https://github.com/abhidevmishra/blog-flog.git
cd blog-flog
```

### 2. Environment Configuration
Create a `.env` file in the root directory:
```env
DEBUG=True
SECRET_KEY=generate-a-secure-key
DB_NAME=django_db
DB_USER=django_user
DB_PASSWORD=django_pass
DB_HOST=db
DB_PORT=5432
GEMINI_API_KEY=your-google-api-key
GEMINI_AI_MODEL=gemini-1.5-flash
```

### 3. Spin Up with Docker
```bash
docker compose up --build -d
```
The `entrypoint.sh` automatically handles:
- ✅ DB Migrations
- ✅ Static File Collection
- ✅ ASGI Server Initialization

---

## 🔧 Developer Commands

| Action | Command |
| :--- | :--- |
| **View Web Logs** | `docker compose logs -f web` |
| **New Migration** | `docker compose exec web python manage.py makemigrations` |
| **Apply Migrations** | `docker compose exec web python manage.py migrate` |
| **Create Admin** | `docker compose exec web python manage.py createsuperuser` |
| **Reset System** | `docker compose down -v` |

---

## 🗺 Roadmap
- [ ] Redis integration for persistent Task Queues (Celery/Django-Q2).
- [ ] Export blogs as PDF/Markdown via CLI.
- [ ] Multi-tenant support for personal subdomains.

---

## 🤝 Contributing
Contributions are welcome! If you find a bug or have a feature request, please open an issue.

Built with ❤️ by [@AbhiMisRaw](https://github.com/AbhiMisRaw)
