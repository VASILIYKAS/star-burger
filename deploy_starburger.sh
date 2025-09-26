#!/bin/bash
set -Eeuo pipefail

cd /var/www/starburger/star-burger

git pull

docker exec -it star-burger-frontend npm ci --include=dev
docker exec -it star-burger-frontend sh -c \
  "./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url='/bundles/'"

docker-compose -f docker-compose.prod.yml build backend frontend
docker-compose -f docker-compose.prod.yml up -d

docker exec -it star-burger-backend python manage.py migrate
docker exec -it star-burger-backend python manage.py collectstatic --noinput

sudo systemctl reload nginx

echo "Деплой успешно завершён!"

set -a
source .env || true
set +a

if [ -n "${ROLLBAR_ACCESS_TOKEN:-}" ]; then
  curl -X POST "https://api.rollbar.com/api/1/deploy" \
    -H "X-Rollbar-Access-Token: $ROLLBAR_ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
      "environment": "production",
      "revision": "'"$(git rev-parse HEAD)"'",
      "local_username": "'"$(whoami)"'",
      "comment": "Automatic deploy"
    }'
  echo "Данные о деплое успешно отправлены в Rollbar."
else
  echo "Переменная ROLLBAR_ACCESS_TOKEN не найдена, пропускаем отправку данных в Rollbar."
fi
exit 0
