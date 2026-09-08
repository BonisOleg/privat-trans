#!/usr/bin/env bash
# Docker Engine + Compose plugin на Ubuntu 24.04 (DigitalOcean Droplet).
set -euo pipefail

if command -v docker >/dev/null 2>&1; then
  echo "==> Docker вже встановлено: $(docker --version)"
  docker compose version
  exit 0
fi

echo "==> Встановлення Docker через офіційний скрипт get.docker.com"
curl -fsSL https://get.docker.com | sh

systemctl enable --now docker
docker --version
docker compose version
