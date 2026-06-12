#!/bin/sh
set -e
cd "$(dirname "$0")/../my_cars"

FORCE=""
if [ "$1" = "--force" ]; then
  FORCE="--force"
fi

echo "==> Импорт fixture..."
python manage.py import_cars $FORCE

echo "==> Готово"
