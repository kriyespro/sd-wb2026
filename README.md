# Winning Blueprints — Winning Blueprints Platform

Django 5 SaaS platform with three portals: public agency website, academy, client/student dashboards, and internal ops.

## Quick start

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_users
python manage.py seed_academy
python manage.py seed_clients
python manage.py seed_ops
python manage.py seed_billing
python durga.py
```

Visit http://127.0.0.1:8000/

## Test logins

See `test_user.txt`. Key accounts:

| User | Password | Portal |
|------|----------|--------|
| admin | admin1234 | /ops/ |
| sales1 | sales1234 | /ops/ (leads) |
| client1 | client1234 | /dashboard/client/ |
| student1 | student1234 | /dashboard/student/ |

## Architecture

- **Public site** (`/`) — agency marketing, lead capture
- **Academy** (`/academy/`) — courses catalog + student portal
- **Client dashboard** (`/dashboard/client/`) — projects, reports, invoices
- **Student dashboard** (`/dashboard/student/`) — courses, assignments, placement
- **Ops portal** (`/ops/`) — quality check, leads, talent pipeline, invoices
- **Admin** (`/sd/`) — Django admin

## Production deploy (Docker)

Full guide: `deploy/DEPLOY.md`

```bash
# 1. Copy and edit secrets in .env.prod
cp .env.prod .env.prod   # fill DJANGO_SECRET_KEY, POSTGRES_PASSWORD, etc.

# 2. Add SSL certs to deploy/certs/ (see deploy/certs/README.md)

# 3. Build and run
docker compose --env-file .env.prod up -d --build

# 4. Seed (first time)
docker compose exec web python manage.py seed_users
docker compose exec web python manage.py seed_academy
docker compose exec web python manage.py seed_clients
docker compose exec web python manage.py seed_ops
docker compose exec web python manage.py seed_billing
```

**Live URLs:** https://winningblueprints.com/ · https://159.195.52.197/

Stack: nginx (HTTPS) → Gunicorn → Django · PostgreSQL · Redis

## Compile Tailwind CSS

```bash
npm install
npm run build:css        # one-time build
npm run watch:css        # dev watch mode
```

## Tests

```bash
python manage.py test
```

## Tech stack

Python 3.12 · Django 5 · Jinja2 · HTMX · Alpine.js · Tailwind CDN · SQLite (dev) / PostgreSQL (prod)
# sd-wb2026
