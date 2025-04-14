**Установка и настройка**

1. Клонируйте репозиторий на ваш сервер:

`git clone https://github.com/shalmeo/auth-service.git`

2. Перейдите в директорию проекта:

`cd auth-service`

3. Запустите приложение:

`docker compose up -d`

4. Приложение будет доступно по адресу: `http://127.0.0.1:9898`,
а также документация `http://127.0.0.1:9898/docs/`


5.Сделайте запрос регистрации пользователя

`curl --location 'http://127.0.0.1:9898/register' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "test@email.ru",
    "role": "patient"
}'`

6. Сделайте запрос на получения пользователя

`curl --location --request GET 'http://127.0.0.1:9898/me' \
--header 'Content-Type: application/json' \
--header 'Cookie: {нужно подставить значение из пред. запроса}' \
`

7. Чтобы запустить тесты создайте окружение и выполните команды:

`pip install -r requirements.txt`

`pytest tests`