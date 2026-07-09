#!/bin/bash
set -e
echo "=== Winning Blueprints Security Check ==="
echo ""

check_env() {
  val=$(grep "^$1=" .env.prod 2>/dev/null | cut -d= -f2-)
  if [[ "$val" == *"REPLACE"* ]] || [[ -z "$val" ]]; then
    echo "❌ $1 — not configured"
    return 1
  else
    echo "✅ $1 — set"
    return 0
  fi
}

fail=0
check_env DJANGO_SECRET_KEY || fail=1
check_env POSTGRES_PASSWORD || fail=1

echo ""
echo "App port: 8888 (localhost only)"
echo "Allowed hosts:"
grep DJANGO_ALLOWED_HOSTS .env.prod
echo ""
echo "CSRF origins:"
grep CSRF_TRUSTED_ORIGINS .env.prod

echo ""
if ss -tlnp 2>/dev/null | grep -q ':8888 '; then
  echo "⚠️  Port 8888 already in use — check for conflicts"
elif lsof -i :8888 >/dev/null 2>&1; then
  echo "⚠️  Port 8888 already in use — check for conflicts"
else
  echo "✅ Port 8888 available"
fi

echo ""
if [[ $fail -eq 0 ]]; then
  echo "Ready. Run: docker compose --env-file .env.prod up -d --build"
  echo "Then configure host nginx using deploy/host-nginx-snippet.conf"
else
  echo "Fix issues above before deploying."
  exit 1
fi
