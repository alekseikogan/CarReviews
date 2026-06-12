#!/bin/sh
# Let's Encrypt для drivelog.live (первый выпуск + включение HTTPS в nginx)
set -e
cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
  echo "Создайте .env (см. .env.example)"
  exit 1
fi

set -a
# shellcheck disable=SC1091
. ./.env
set +a

if [ -z "$DOMAIN" ] || [ -z "$CERTBOT_EMAIL" ]; then
  echo "Добавьте в .env: DOMAIN=drivelog.live и CERTBOT_EMAIL=your@email.com"
  exit 1
fi

if ! command -v envsubst >/dev/null 2>&1; then
  echo "Установите gettext-base: sudo apt install -y gettext-base"
  exit 1
fi

echo "==> Убедитесь, что порт 443 открыт в Security Group EC2"
echo "==> Перезапуск nginx (HTTP + webroot для certbot)..."
docker compose up -d nginx

echo "==> Получение сертификата для ${DOMAIN} и www.${DOMAIN} ..."
docker compose --profile ssl run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  --email "$CERTBOT_EMAIL" \
  --agree-tos \
  --no-eff-email \
  -d "$DOMAIN" \
  -d "www.$DOMAIN"

echo "==> Включение HTTPS в nginx.conf ..."
export DOMAIN
envsubst '${DOMAIN}' < nginx/nginx.ssl.conf.template > nginx.conf

echo "==> Перезапуск nginx с SSL ..."
docker compose restart nginx

echo "==> Автообновление сертификата (certbot renew) ..."
docker compose --profile ssl up -d certbot

echo ""
echo "Готово: https://${DOMAIN}/ и https://www.${DOMAIN}/"
echo ""
echo "Обновите .env и перезапустите backend:"
echo "  CORS_ALLOWED_ORIGINS=https://${DOMAIN},https://www.${DOMAIN}"
echo "  CSRF_TRUSTED_ORIGINS=https://${DOMAIN},https://www.${DOMAIN}"
echo "  docker compose up -d backend"
