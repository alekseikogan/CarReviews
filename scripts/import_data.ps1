# Импорт данных из fixtures/cars.json и привязка локальных фото
param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot\..\my_cars"

$args_list = @("import_cars")
if ($Force) { $args_list += "--force" }

Write-Host "==> Импорт fixture..."
python manage.py @args_list

Write-Host "==> Готово"
