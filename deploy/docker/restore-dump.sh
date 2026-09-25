#!/usr/bin/env bash
# Відновлює Postgres з дампа тестового Droplet. Медіа — окремий tar, якщо є.
set -euo pipefail

cd "$(dirname "$0")/../.."

DUMP="${1:-deploy/dumps/privattrans-164.92.161.44-2026-09-25.sql.gz}"
MEDIA="${2:-deploy/dumps/media.tgz}"
COMPOSE=(docker compose -f docker-compose.yml -f docker-compose.prod.yml)

if [ "${RESTORE_YES:-}" != "1" ]; then
  echo "FATAL: стирає поточну БД. Запуск: RESTORE_YES=1 bash deploy/docker/restore-dump.sh"
  exit 1
fi
if [ ! -f "$DUMP" ]; then
  echo "FATAL: немає ${DUMP}"
  exit 1
fi

echo "==> stop backend"
"${COMPOSE[@]}" stop backend

echo "==> recreate database from ${DUMP}"
"${COMPOSE[@]}" exec -T db sh -c 'psql -U "$POSTGRES_USER" -d postgres -v ON_ERROR_STOP=1 -c "DROP DATABASE IF EXISTS \"$POSTGRES_DB\" WITH (FORCE);" -c "CREATE DATABASE \"$POSTGRES_DB\" OWNER \"$POSTGRES_USER\";"'
gzip -dc "$DUMP" | "${COMPOSE[@]}" exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v ON_ERROR_STOP=1'

"${COMPOSE[@]}" start backend

if [ -f "$MEDIA" ]; then
  echo "==> media from ${MEDIA}"
  "${COMPOSE[@]}" cp "$MEDIA" backend:/tmp/media.tgz
  "${COMPOSE[@]}" exec -T backend sh -c "mkdir -p /app/media && tar xzf /tmp/media.tgz -C /app/media"
else
  echo "==> ${MEDIA} немає — фото і відео треба покласти в volume media окремо"
fi

echo "==> restore done"
