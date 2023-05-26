# Near cars

Для тестового задания

<h4>1. Как запустить сервис?</h4>
   <pre>
      - git clone https://github.com/pavelbeard/near_cars_core
      - cd near_cars_core
      - docker-compose up -d --build
   </pre> 
<h4>2. Переменные окружения.</h4>  
<p>Для core.env:</p>
<pre>
ALLOWED_HOSTS: разрешенные хосты, пишем через пробел

DEBUG: 1 - True, 0 - False

DB_NAME: имя базы данных
DB_USER: пользователь БД
DB_PASSWORD: пароль от БД
DB_HOST: адрес БД
DB_PORT: порт

CACHE_LOCATION: адрес брокера сообщений, в данном проекте используется redis - redis://<адрес_брокера>/0
CELERY_BROKER_UR: redis://<адрес_брокера>/0
CELERY_RESULT_BACKEND: redis://<адрес_брокера>/0

DJANGO_SUPERUSER_USERNAME: имя администратора API
DJANGO_SUPERUSER_EMAIL: почта
DJANGO_SUPERUSER_PASSWORD: пароль

SERVER_ADDRESS: адрес API
SERVER_PORT: порт API
</pre>
<p>Для worker.env:</p>
<pre>
DEBUG: как в core.env

DB_NAME: имя базы данных
DB_USER: пользователь БД
DB_PASSWORD: пароль от БД
DB_HOST: адрес БД
DB_PORT: порт

CACHE_LOCATION: адрес брокера сообщений, в данном проекте используется redis - redis://<адрес_брокера>/0
CELERY_BROKER_UR: redis://<адрес_брокера>/0
CELERY_RESULT_BACKEND: redis://<адрес_брокера>/0
</pre>
<p>Для psql.env:</p>
<pre>
POSTGRES_DB: имя базы данных PostgreSQL
POSTGRES_USER: администратор БД
POSTGRES_PASSWORD: пароль
</pre>
<h4>3. Документация</h4>
Находится по адресу: 
<pre>
    http://<:api_address:port>/api/docs
</pre>
<h4>4. Команды</h4>
Добавил следующие команды в manage.py: 
<pre>
    createtasks - Создает задачу обновления локаций у машин
    addlocations - Добавляет локации в БД из csv файла
    addcars - Добавляет машины в БД из csv файла
    updatelocations - Обновляет локации у машин случайным образом
</pre>

