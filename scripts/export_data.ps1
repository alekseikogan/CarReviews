# Экспорт данных и фото в fixtures/cars.json + media/cars/
$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot\..\my_cars"

Write-Host "==> Привязка локальных фото..."
python manage.py download_car_photos --link-only

Write-Host "==> Экспорт fixture..."
python manage.py export_cars

Write-Host "==> Готово: fixtures/cars.json и media/cars/"
