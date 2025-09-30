# Сайт доставки еды Star Burger

Это сайт сети ресторанов Star Burger. Здесь можно заказать превосходные бургеры с доставкой на дом.\
Ссылка на сайт: https://starburger-dvm.ru/

![скриншот сайта](https://dvmn.org/filer/canonical/1594651635/686/)


Сеть Star Burger объединяет несколько ресторанов, действующих под единой франшизой. У всех ресторанов одинаковое меню и одинаковые цены. Просто выберите блюдо из меню на сайте и укажите место доставки. Мы сами найдём ближайший к вам ресторан, всё приготовим и привезём.

На сайте есть три независимых интерфейса. Первый — это публичная часть, где можно выбрать блюда из меню, и быстро оформить заказ без регистрации и SMS.

Второй интерфейс предназначен для менеджера. Здесь происходит обработка заказов. Менеджер видит поступившие новые заказы и первым делом созванивается с клиентом, чтобы подтвердить заказ. После оператор выбирает ближайший ресторан и передаёт туда заказ на исполнение. Там всё приготовят и сами доставят еду клиенту.

Третий интерфейс — это админка. Преимущественно им пользуются программисты при разработке сайта. Также сюда заходит менеджер, чтобы обновить меню ресторанов Star Burger.


## Оглавление

- [Переменные окружения](#переменные-окружения)
- [Как запустить dev-версию сайта](#как-запустить-dev-версию-сайта)
- [Как запустить prod-версию сайта](#как-запустить-prod-версию-сайта)
- [Быстрое обновление кода на сервере](#быстрое-обновление-кода-на-сервере)
- [Цель проекта](#цель-проекта)


## Переменные окружения
Проект использует файл `.env` для хранения конфиденциальных данных. В репозитории уже есть шаблон `example.env`, который нужно скопировать и настроить:
1. Скопируйте файл example.env в .env:
- Для macOS и Linux выполните команду:
```bash
cp example.env .env
```
- Для Windows используйте команду:
```powershell
copy example.env .env
```
2. Откройте файл `.env` в текстовом редакторе.
3. Укажите значение переменных после знака `=`:

Определите переменную окружения `SECRET_KEY`. Создать файл `.env` в каталоге `star_burger/` и положите туда такой код:
```sh
SECRET_KEY=django-insecure-0if40nf4nf93n4
```
`YANDEX_APIKEY` - переменная окружения с API-ключом от Яндекса Геокодер, получить можно [здесь](https://developer.tech.yandex.ru/services).
```sh
YANDEX_APIKEY=ваш_ключ
```
Добавьте переменную окружения `DEBUG`:
- `True` — для локального запуска
- `False` — для запуска на сервере\
По умолчанию установлено True.
```sh
DEBUG=значение
```
`ROLLBAR_ACCESS_TOKEN` - переменная окружения с ключом [Rollbar](rollbar.com), ключ можно создать в настройках вашего проекта в разделе "Project Access Tokens"
```sh
ROLLBAR_ACCESS_TOKEN=ваш_ключ
```
Так же при необходимости добавьте переменную окружения с значением "production" для продакшн версии или "local" для dev-версии сайта по умолчанию задана "local" версия. Это значение будет отображаться на сайте rollbar 
```sh
ENVIRONMENT=значение
```

`ALLOWED_HOSTS` — список доменов и IP-адресов, с которых разрешён доступ. Например:
```sh
ALLOWED_HOSTS=starburger-dvm.ru,www.starburger-dvm.ru,127.0.0.1,localhost
```
`POSTGRES_DB` - Укажите имя для базы данных PostgreSQL. \
Можете использовать любое, например:
```sh
POSTGRES_DB=starburgerdb
```
`POSTGRES_USER` - Укажите имя пользователя PostgreSQL. \
Можете использовать любое, например:
```sh
POSTGRES_USER=starburgeruser
```
`POSTGRES_PASSWORD` - Укажите пароль пользователя PostgreSQL.
Можете использовать любой, например:
```sh
POSTGRES_PASSWORD=starburger
```
`POSTGRES_DB` - Строка подключения к базе данных базы данных PostgreSQL. \
Состоит из имени пользователя, пароля, хоста, порта и имени базы данных.
```sh
DB_URL=postgresql://starburgeruser:starburger@db:5432/starburgerdb
```


## Как запустить dev-версию сайта
Сборка происходит с помощью запуска `docker-compose.dev.yml`, который находится в папке `docker`\
Докер должен быть установлен! Скачать можно [здесь](https://www.docker.com/get-started/).\
Перед запуском **укажите все переменные окружения**.
Команда для запуска:
```bash
docker-compose -f docker-compose.dev.yml up --build
```
Для создания суперпользователя в джанго, нужно выполнить команду из контейнера:
```sh
docker exec -it star-burger-backend python manage.py createsuperuser
```
Сайт будет доступен по адресу - https://localhost/\
Админка - https://localhost/admin


## Как запустить prod-версию сайта
Сборка происходит с помощью запуска `docker-compose.prod.yml`, который находится в папке `docker`\
Перед запуском `docker-compose.prod.yml` небходимо сделать несколько шагов:
1. Обновить систему:
```bash
apt update && apt upgrade -y
```
2. Устанавить Docker и Docker Compose:
```bash
apt install -y docker.io docker-compose
systemctl enable docker
systemctl start docker
```
3. Скопировать проект на сервер:
```bash
cd /var/www/starburger
git clone https://github.com/VASILIYKAS/star-burger.git
```
4. Запустить `docker-compose.prod.yml`, команда:
```bash 
docker-compose -f docker-compose.prod.yml up --build
```
5. Установить Nginx:
```bash
apt install -y nginx
```
6. Установить Certbot для SSL сертификатов:
```bash
apt install -y certbot python3-certbot-nginx
```
7. Теперь необходимо настроить Nginx, создаем файл:
```bash
nano /etc/nginx/sites-available/starburger.conf
```
Содержимое примерно такое
```sh
server {
    listen 80;
    server_name ваш_домен_или_IP;

    # Папка где располгаются статические файлы
    location /static/ {
        alias /var/www/starburger/star-burger/backend/staticfiles/;
    }

    # Папка где располгаются файлы media
    location /media/ {
        alias /var/www/starburger/star-burger/backend/media/;
    }

    # Папка где располгаются собраные frontend файлы
    location /bundles/ {
        alias /var/www/starburger/star-burger/frontend/bundles/;
    }

    # Запросы к API проксируются напрямую в backend через Gunicorn
    location /api/ {
        include /etc/nginx/proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }

    # Все остальные запросы проксируются напрямую в backend через Gunicorn
    location / {
        include /etc/nginx/proxy_params;
        proxy_pass http://127.0.0.1:8000/;
    }
}
```
8. Создать симлинк (ярлык):
```bash
ln -s /etc/nginx/sites-available/starburger.conf /etc/nginx/sites-enabled/
```
9. Получить SSL сертификаты:
```bash
certbot --nginx -d ваш_домен_или_IP
```
Certbot автоматически пропишет SSL в конфиг Nginx.
10. Перезапустить Nginx:
```bash
systemctl reload nginx
```
11. Проверка: 
Открываем браузер: https://ваш_домен_или_IP/

Статус контейнеров:
```bash
docker ps
docker-compose -f docker-compose.prod.yml logs -f
```
Статус Nginx и Certbot:
```bash
systemctl status nginx
```


## Быстрое обновление кода на сервере

Для быстрого обновления кода на сервере используется скрипт `deploy_starburger.sh`. Он выполняет все необходимые действия:
1. **Обновление кода**  
   - Получает изменения из Git-репозитория (`git pull`)

2. **Установка зависимостей**  
   - Python: `docker exec -it star-burger-backend pip install -r requirements.txt`  
   - Node.js: `docker-compose -f docker-compose.prod.yml up --build frontend`

3. **Сборка проекта**  
   - Пересобирает статику Django (`docker exec -it star-burger-backend python manage.py collectstatic --noinput`)  

4. **Миграции базы данных**  
   - Автоматически применяет миграции (`docker exec -it star-burger-backend python manage.py migrate`)

5. **Перезапуск сервисов**    
   - Nginx: `systemctl reload nginx`

6. **Отчёт о результате**  
   - Выводит сообщение при успешном завершении 
   - Немедленно прерывается при ошибках (`set -Eeuo pipefail`)

7. **Отправка данных о деплое в Rollbar**
   - Узнаёт хэш коммита
   - Отправляет данные в Rollbar

Для запуска скрипта перейдите в папку проекта и используйте команду:
```bash
./deploy_starburger.sh
```


## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org). За основу был взят код проекта [FoodCart](https://github.com/Saibharath79/FoodCart).

Где используется репозиторий:

- Второй и третий урок [учебного курса Django](https://dvmn.org/modules/django/)
