#!/bin/bash
# Quick security checklist — run on server before go-live
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
echo "Allowed hosts:"
grep DJANGO_ALLOWED_HOSTS .env.prod

echo ""
echo "CSRF origins:"
grep CSRF_TRUSTED_ORIGINS .env.prod

echo ""
if [[ -f deploy/certs/fullchain.pem ]] && [[ -f deploy/certs/privkey.pem ]]; then
  echo "✅ SSL certificates found"
else
  echo "❌ SSL certificates missing in deploy/certs/"
  fail=1
fi

echo ""
if [[ $fail -eq 0 ]]; then
  echo "All checks passed. Run: docker compose --env-file .env.prod up -d --build"
else
  echo "Fix issues above before deploying."
  exit 1
fi
