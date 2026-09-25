#!/usr/bin/env bash
# HTTP-first деплой PrivatTrans на Droplet (Docker Compose + nginx).
# SSL/домен — окремо, django-docker-ssl. Push на GitHub ≠ live.
set -euo pipefail

cd "$(dirname "$0")/../.."

COMPOSE=(docker compose -f docker-compose.yml -f docker-compose.prod.yml)
if [ -f .env ] && grep -qE '^USE_HTTPS=true' .env; then
  COMPOSE+=(-f docker-compose.ssl.yml)
fi
EXPECTED_SERVICES=(db backend nginx)

if [ "${1:-}" = "--pull" ]; then
  if [ -d .git ]; then
    echo "==> git pull origin main"
    git fetch origin
    git checkout main
    git pull --ff-only origin main
  else
    echo "FATAL: --pull потребує git-клону в /var/www/privat-trans"
    exit 1
  fi
fi

if [ ! -f .env ]; then
  echo "FATAL: немає .env — cp .env.docker.example .env і заповни IP + секрети"
  exit 1
fi

if grep -E '^(SECRET_KEY|POSTGRES_PASSWORD|DATABASE_URL|ALLOWED_HOSTS|CSRF_TRUSTED_ORIGINS)=' .env | grep -qE 'DROPLET_IP|CHANGE_ME'; then
  echo "FATAL: у .env лишилися плейсхолдери (DROPLET_IP / CHANGE_ME)"
  exit 1
fi

if ! grep -qE 'ALLOWED_HOSTS=.*[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' .env; then
  echo "FATAL: ALLOWED_HOSTS має містити IPv4 Droplet (не лише localhost)"
  exit 1
fi

csrf_ip="$(
  grep -E '^CSRF_TRUSTED_ORIGINS=' .env \
    | grep -oE 'http://[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' \
    | grep -vE 'http://127\.' \
    | head -1 || true
)"
if [ -z "${csrf_ip}" ]; then
  echo "FATAL: CSRF_TRUSTED_ORIGINS має містити http://<публічний IPv4>"
  exit 1
fi

DROPLET_IP="$(
  grep -E '^ALLOWED_HOSTS=' .env \
    | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' \
    | grep -vE '^127\.' \
    | head -1 || true
)"
if [ -z "${DROPLET_IP}" ]; then
  echo "FATAL: не вдалося вичитати публічний IPv4 з ALLOWED_HOSTS"
  exit 1
fi

echo "==> Звільняємо порти 80/443 від host nginx/gunicorn"
systemctl stop nginx 2>/dev/null || true
systemctl disable nginx 2>/dev/null || true
systemctl stop gunicorn 2>/dev/null || true

echo "==> Build backend + nginx"
"${COMPOSE[@]}" build backend nginx

echo "==> Up (перший up нефатальний — ERR-52)"
"${COMPOSE[@]}" up -d --force-recreate || echo "WARN: перший up повернув помилку — фінальний up нижче"

echo "==> Чекаємо backend /healthz/ ..."
ok=0
for _ in $(seq 1 40); do
  if "${COMPOSE[@]}" exec -T backend \
    python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz/', timeout=2)" \
    >/dev/null 2>&1; then
    echo "==> backend OK"
    ok=1
    break
  fi
  sleep 3
done
if [ "$ok" -ne 1 ]; then
  echo "FATAL: backend не відповів на /healthz/ за ~2 хв"
  "${COMPOSE[@]}" logs --tail=80 backend
  exit 1
fi

"${COMPOSE[@]}" up -d

echo "==> Інвентаризація сервісів (inspect Status, не grep compose ps)"
"${COMPOSE[@]}" ps
missing=0
for svc in "${EXPECTED_SERVICES[@]}"; do
  cid="$("${COMPOSE[@]}" ps -q "$svc" 2>/dev/null || true)"
  if [ -z "$cid" ]; then
    echo "WARN: сервіс відсутній: $svc"
    missing=1
    continue
  fi
  state="$(docker inspect -f '{{.State.Status}}' "$cid" 2>/dev/null || echo missing)"
  if [ "$state" != "running" ]; then
    echo "WARN: сервіс не running ($state): $svc"
    missing=1
  fi
done
if [ "$missing" -ne 0 ]; then
  echo "FATAL: не всі сервіси running"
  "${COMPOSE[@]}" logs --tail=50
  exit 1
fi

echo "==> Django check"
"${COMPOSE[@]}" exec -T backend python3 manage.py check

echo "==> Smoke Host=${DROPLET_IP}"
curl -sf http://127.0.0.1/healthz/ && echo " healthz OK" || echo "WARN: healthz failed"
curl -sI -H "Host: ${DROPLET_IP}" http://127.0.0.1/ | head -5

echo "==> Далі: RESTORE_YES=1 bash deploy/docker/restore-dump.sh (дамп тестового сервера), не seed_demo"
echo "==> Логи: ${COMPOSE[*]} logs -f backend nginx"
