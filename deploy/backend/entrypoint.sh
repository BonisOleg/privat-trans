#!/bin/sh
set -e
if [ -n "$DATABASE_URL" ] && echo "$DATABASE_URL" | grep -q "postgres"; then
  echo "Waiting for postgres..."
  while ! nc -z db 5432; do sleep 0.1; done
  echo "PostgreSQL started"
fi
python3 manage.py compilemessages -l en 2>/dev/null || true
exec "$@"
