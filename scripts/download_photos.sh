#!/bin/sh
set -e
cd "$(dirname "$0")/../my_cars"

FORCE=""
if [ "$1" = "--force" ]; then
  FORCE="--force"
fi

python manage.py download_car_photos $FORCE
