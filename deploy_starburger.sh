#!/bin/bash
set -Eeuo pipefail

cd /opt/star-burger

git pull

npm ci --include=dev

./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"

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
