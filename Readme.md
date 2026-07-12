# anjlapastora.github.io

Personal site and journal — built with Wagtail CMS.

## Tech stack

- **Django 5.2** + **Wagtail 7.3** — CMS, page tree, and admin
- **SQLite** locally, **Postgres** (via `psycopg2-binary` / `dj-database-url`) in production
- **wagtail-markdown** — Markdown post bodies
- **wagtail-favicon** — favicon management
- **django-storages** + **boto3** — S3-compatible media storage in production
- **whitenoise** — static file serving
- **gunicorn** — production app server
- Plain CSS/JS (no frontend build step) — see `anj_lapastora/anj_lapastora/static/`

## Project structure

The Django/Wagtail project lives in `anj_lapastora/`. Page types (Home, Tech, Musings, Atelier/Photo, About) are defined in `anj_lapastora/home/models.py`, with templates in `anj_lapastora/home/templates/home/`.

## Running locally

```bash
cd anj_lapastora
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run with the local settings module:

```bash
export DJANGO_SETTINGS_MODULE=anj_lapastora.settings.local
export SECRET_KEY=dev-secret-key   # any value works locally

python manage.py migrate
python manage.py createsuperuser   # first time only
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the site and `http://127.0.0.1:8000/admin/` for the Wagtail admin.

Local settings (`anj_lapastora/settings/local.py`) use a SQLite database at `anj_lapastora/db.sqlite3` and store media on the local filesystem — no external services needed for day-to-day development.

## Running tests

```bash
python manage.py test
```

Tests build their own throwaway page tree per test case (see `home/tests/factories.py`) and run against an in-memory database, so they never touch `db.sqlite3`. Coverage includes the `home` page/context models, view rendering for every page type, the `bootstrap_site` management command, and the search view.

## Production

`build.sh` installs dependencies, collects static files, runs migrations, and bootstraps the initial site/homepage. `start.sh` runs the app via gunicorn. A `Dockerfile` is also provided for containerized deploys.
