#!/bin/bash
set -Eeuo pipefail

cd /opt/star-burger

git pull

npm ci --dev

source .venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py collectstatic --noinput --clear

sudo systemctl restart gunicorn

sudo systemctl reload nginx

echo "Деплой успешно завершён!"
exit 0
