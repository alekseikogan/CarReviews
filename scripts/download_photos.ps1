# Скачать все фото в media/cars/
param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot\..\my_cars"

$args_list = @("download_car_photos")
if ($Force) { $args_list += "--force" }

python manage.py @args_list
