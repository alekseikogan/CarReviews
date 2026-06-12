#!/bin/sh
set -e
cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
  echo "Создайте .env из .env.example и укажите RDS credentials"
  exit 1
fi

echo "==> Сборка React (frontend/dist)..."
cd frontend
npm ci
npm run build
cd ..

echo "==> Запуск контейнеров..."
docker compose up -d --build

echo "==> Готово: http://<ваш-ec2-ip>/"
