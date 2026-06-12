#!/bin/sh
set -e
cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
  echo "Создайте .env из .env.example и укажите RDS credentials"
  exit 1
fi

echo "==> Сборка и запуск контейнеров (React собирается внутри образа nginx)..."
docker compose up -d --build

echo "==> Готово: http://<ваш-ec2-ip>/"
