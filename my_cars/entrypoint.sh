#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
while ! python -c "
import socket, os
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1)
try:
    s.connect((os.environ.get('POSTGRES_HOST', 'db'), int(os.environ.get('POSTGRES_PORT', '5432'))))
    s.close()
except Exception:
    exit(1)
" 2>/dev/null; do
  sleep 1
done
echo "PostgreSQL is up"

python manage.py migrate --noinput

if [ -f fixtures/cars.json ]; then
  python manage.py import_cars
else
  python manage.py load_cars
  python manage.py download_car_photos
fi

python manage.py collectstatic --noinput

exec gunicorn my_cars.wsgi:application --bind 0.0.0.0:8000 --workers 2
