#!/usr/bin/env bash
# Перенос локальної CMS-вітрини в Postgres контейнера.
# Ліди (PII) і auth.User у dump не входять.
# Порядок на сервері: healthz OK → import → createsuperuser (ніколи навпаки).
set -euo pipefail

cd "$(dirname "$0")/../.."

DUMP_DIR="deploy/dumps"
DUMP_JSON="${DUMP_DIR}/cms.json"
MEDIA_TGZ="${DUMP_DIR}/media.tgz"
COMPOSE=(docker compose -f docker-compose.yml -f docker-compose.prod.yml)
APPS=(core services faq careers social_proof calculator)

usage() {
  echo "Usage: $0 export | import [--yes] | push <host:/var/www/privat-trans> [--yes]"
  exit 1
}

ensure_dump_dir() {
  mkdir -p "$DUMP_DIR"
}

cmd_export() {
  ensure_dump_dir
  echo "==> dumpdata → ${DUMP_JSON}"
  python3 manage.py dumpdata "${APPS[@]}" \
    --natural-foreign --natural-primary --indent 2 \
    -o "$DUMP_JSON"
  if [ -d media ] && [ -n "$(ls -A media 2>/dev/null || true)" ]; then
    tar czf "$MEDIA_TGZ" -C media .
    echo "==> media → ${MEDIA_TGZ}"
  else
    echo "==> media порожня — пропускаю tar"
  fi
}

cmd_import() {
  if [ "${1:-}" != "--yes" ]; then
    echo "FATAL: import робить flush. Підтвердь: $0 import --yes"
    exit 1
  fi
  if [ ! -f "$DUMP_JSON" ]; then
    echo "FATAL: немає ${DUMP_JSON} — спочатку export або scp"
    exit 1
  fi
  echo "==> flush (стирає auth.User) + loaddata"
  "${COMPOSE[@]}" exec -T backend python3 manage.py flush --noinput
  "${COMPOSE[@]}" cp "$DUMP_JSON" backend:/tmp/cms.json
  "${COMPOSE[@]}" exec -T backend python3 manage.py loaddata /tmp/cms.json
  if [ -f "$MEDIA_TGZ" ]; then
    "${COMPOSE[@]}" cp "$MEDIA_TGZ" backend:/tmp/media.tgz
    "${COMPOSE[@]}" exec -T backend sh -c "mkdir -p /app/media && tar xzf /tmp/media.tgz -C /app/media"
  fi
  echo "==> Імпорт завершено. ТЕПЕР: createsuperuser (ERR-119)"
}

cmd_push() {
  target="${1:-}"
  confirm="${2:-}"
  if [ -z "$target" ]; then
    usage
  fi
  if [ ! -f "$DUMP_JSON" ]; then
    echo "FATAL: немає ${DUMP_JSON} — спочатку $0 export"
    exit 1
  fi
  remote_host="${target%%:*}"
  remote_path="${target#*:}"
  echo "==> scp dumps → ${target}"
  ssh "$remote_host" "mkdir -p ${remote_path}/deploy/dumps"
  scp "$DUMP_JSON" "${target}/deploy/dumps/cms.json"
  if [ -f "$MEDIA_TGZ" ]; then
    scp "$MEDIA_TGZ" "${target}/deploy/dumps/media.tgz"
  fi
  if [ "$confirm" = "--yes" ]; then
    ssh "$remote_host" "cd ${remote_path} && bash deploy/docker/sync-data.sh import --yes"
  else
    echo "==> На сервері: cd ${remote_path} && bash deploy/docker/sync-data.sh import --yes"
    echo "==> Потім createsuperuser"
  fi
}

case "${1:-}" in
  export) cmd_export ;;
  import) cmd_import "${2:-}" ;;
  push) cmd_push "${2:-}" "${3:-}" ;;
  *) usage ;;
esac
