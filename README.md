# News Site

Django news site with posts, comments, likes, pagination, media uploads, search, categories, pinned posts, drafts, view counter, video thumbnails, and AJAX likes.

## Stack

- Python 3.12
- Django 6.0
- SQLite for local development
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

Create local environment file:

```bash
cp .env.example .env
```

For local development, the defaults in `.env.example` are enough. For production, change `DJANGO_SECRET_KEY`, set `DJANGO_DEBUG=False`, and configure `DJANGO_ALLOWED_HOSTS`.

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

## Git Notes

The repository should include source code, templates, static assets, migrations, `requirements.txt`, `.env.example`, and this README.

The repository should not include:

- `venv/`
- `.env`
- `db.sqlite3`
- uploaded files in `media/`
- Python cache files
