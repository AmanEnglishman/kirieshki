# News Site

Django news site with posts, comments, likes, pagination, media uploads, search, categories, pinned posts, drafts, view counter, video thumbnails, and AJAX likes.

## Stack

- Python 3.12
- Django 6.0
- SQLite for local development
- PostgreSQL on Render when `DATABASE_URL` is configured
- Django Templates
- HTML/CSS with minimal JavaScript

## Features

- Admin CRUD for posts
- Optional post image, video, and video thumbnail
- Published/draft posts
- Pinned posts shown first
- Categories and category filter
- Search by title and content
- Post detail page with comments and related posts
- Anonymous comments
- Cookie-based likes without page reload
- View counter
- Responsive layout

## Local Setup

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Create admin user:

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

Open:

- Site: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

## Tests

```bash
python manage.py test
```

## Render Deploy

Root Directory: leave this field empty. The project root already contains `manage.py`.

Build Command:

```bash
./build.sh
```

Start Command:

```bash
python -m gunicorn news_site.asgi:application -k uvicorn.workers.UvicornWorker
```

Optional but recommended: create a Render PostgreSQL database and add its Internal Database URL as `DATABASE_URL` in the web service environment variables.

For uploaded images and videos, add a Render Persistent Disk mounted at:

```text
/opt/render/project/src/media
```

## Git Notes

The repository should include source code, templates, static assets, migrations, `requirements.txt`, `build.sh`, and this README.

The repository should not include:

- `venv/`
- `.env`
- `db.sqlite3`
- uploaded files in `media/`
- Python cache files
