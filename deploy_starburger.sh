#!/bin/bash
set -Eeuo pipefail

cd /opt/star-burger

git pull

npm ci --include=dev

npm run build 

source .venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py collectstatic --noinput --clear

sudo systemctl restart gunicorn

sudo systemctl reload nginx

echo "Деплой успешно завершён!"

set -a
source /opt/star-burger/.env || true
set +a

if [ -z "${ROLLBAR_ACCESS_TOKEN:-}" ]; then
  echo "Ошибка: переменная ROLLBAR_ACCESS_TOKEN не найдена в файле .env" >&2
  exit 1
fi

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
exit 0
