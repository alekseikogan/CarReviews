#!/bin/sh
set -e
cd "$(dirname "$0")/../my_cars"

echo "==> Привязка локальных фото..."
python manage.py download_car_photos --link-only

echo "==> Экспорт fixture..."
python manage.py export_cars

echo "==> Готово: fixtures/cars.json и media/cars/"
