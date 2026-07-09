#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
until python -c "
import os, socket
host = os.environ.get('POSTGRES_HOST', 'db')
port = int(os.environ.get('POSTGRES_PORT', '5432'))
s = socket.socket()
s.settimeout(2)
try:
    s.connect((host, port))
    print('PostgreSQL is up')
except Exception:
    raise SystemExit(1)
finally:
    s.close()
" 2>/dev/null; do
  sleep 2
done

echo "Waiting for Redis..."
until python -c "
import os, socket
from urllib.parse import urlparse
url = os.environ.get('REDIS_URL', 'redis://redis:6379/1')
parsed = urlparse(url)
host = parsed.hostname or 'redis'
port = parsed.port or 6379
s = socket.socket()
s.settimeout(2)
try:
    s.connect((host, port))
    print('Redis is up')
except Exception:
    raise SystemExit(1)
finally:
    s.close()
" 2>/dev/null; do
  sleep 2
done

export DJANGO_ENV=prod

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn core.wsgi:application -c gunicorn.conf.py
