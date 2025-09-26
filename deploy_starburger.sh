#!/bin/bash
set -Eeuo pipefail

cd /var/www/starburger/star-burger

git pull

docker-compose -f docker-compose.prod.yml rm -f frontend
docker-compose -f docker-compose.prod.yml up --build frontend

docker exec -it star-burger-backend pip install -r requirements.txt
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
