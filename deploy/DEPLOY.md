# Production Deployment

Deploy to **https://winningblueprints.com/** and **https://159.195.52.197/** using Docker.

## 1. Server prerequisites

- Ubuntu 22.04+ (or similar)
- Docker + Docker Compose v2
- Ports 80 and 443 open

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

## 2. Configure environment

Copy `.env.prod` to the server and fill in secrets:

```bash
# Generate Django secret key
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Edit .env.prod — set:
#   DJANGO_SECRET_KEY
#   POSTGRES_PASSWORD
#   EMAIL_HOST_PASSWORD
```

Key values already set:
- `DJANGO_ALLOWED_HOSTS=winningblueprints.com,www.winningblueprints.com,159.195.52.197`
- `CSRF_TRUSTED_ORIGINS=https://winningblueprints.com,https://www.winningblueprints.com,https://159.195.52.197`

## 3. SSL certificates

See `deploy/certs/README.md`. Place `fullchain.pem` and `privkey.pem` in `deploy/certs/`.

## 4. Build and start

```bash
docker compose --env-file .env.prod up -d --build
```

## 5. Seed data (first deploy only)

```bash
docker compose exec web python manage.py seed_users
docker compose exec web python manage.py seed_academy
docker compose exec web python manage.py seed_clients
docker compose exec web python manage.py seed_ops
docker compose exec web python manage.py seed_billing
```

## 6. Verify

```bash
docker compose ps
docker compose logs -f web
curl -I https://winningblueprints.com/
```

## Architecture

| Service | Role |
|---------|------|
| **nginx** | HTTPS termination, static/media, security headers |
| **web** | Gunicorn + Django |
| **db** | PostgreSQL 16 |
| **redis** | Cache + sessions |

## Performance

- Compiled Tailwind CSS (no CDN)
- Redis session + cache backend
- Gzip middleware
- PostgreSQL connection pooling (`CONN_MAX_AGE=600`)
- Nginx static file caching (30 days)
- Gunicorn: 3 workers × 2 threads

## Security

- `DEBUG=False`, strong `SECRET_KEY`
- HSTS, secure cookies, CSRF trusted origins
- `X-Frame-Options: DENY`, `nosniff`, referrer policy
- Non-root containers, secrets via `.env.prod` (not committed)

## Updates

```bash
git pull
docker compose --env-file .env.prod up -d --build
```

## Local CSS rebuild

```bash
npm install
npm run build:css
```
