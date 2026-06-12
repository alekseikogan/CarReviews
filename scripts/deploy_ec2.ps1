# Деплой на EC2: сборка React + docker compose
$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot\.."

if (-not (Test-Path ".env")) {
    Write-Error "Создайте .env из .env.example и укажите RDS credentials"
}

Write-Host "==> Сборка и запуск контейнеров (React собирается внутри образа nginx)..."
docker compose up -d --build

Write-Host "==> Готово: http://<ваш-ec2-ip>/"
