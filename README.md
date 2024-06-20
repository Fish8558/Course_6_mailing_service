## Сервис рассылки сообщений на фреймворке Django

### Технологии

- Django
- PostgreSQL
- Redis
- APScheduler

### Инструкция для запуска проекта:

- Клонировать проект
- Настроить виртуальное окружение и установить зависимости
- Отредактировать файл .env.sample
- Настроить БД
- Запустить проект
- Описание работы

### Клонирование проекта

Клонируйте репозиторий используя следующую команду.

  ```text
  git clone https://github.com/Fish8558/Course_6_mailing_service.git
  ```

### Настройка виртуального окружение и установка зависимостей:
- [Инструкция по установке](https://sky.pro/media/kak-sozdat-virtualnoe-okruzhenie-python/)

### Редактирование .env.sample:

- В корне проекта переименуйте файл .env.sample в .env и отредактируйте параметры:
    ```text
    # Postgresql
    DB_NAME="db_name" - название вашей БД
    DB_USER="postgres" - имя пользователя БД
    DB_PASSWORD="secret" - пароль пользователя БД
    DB_HOST="host" - можно указать "localhost" или "127.0.0.1"
    DB_PORT=port - указываете порт для подключения по умолчанию 5432
    
    # Django
    SECRET_KEY=secret_key - секретный ключ django проекта
    DEBUG=True - режим DEBUG
  
    # Mailing  
    EMAIL_HOST_USER='your_email@yandex.ru' - ваш email yandex
    EMAIL_HOST_PASSWORD='your_yandex_smtp_password' - ваш пароль smtp (подробнее о настройке ниже)
    
    # Superuser
    ADMIN_EMAIL='admin@test.com' - email регистрации администратора сайта
    ADMIN_PASSWORD='secret' - пароль регистрации администратора сайта
    
    # Redis
    REDIS_HOST=redis://host:port - данные местоположения redis
    CACHE_ENABLED=True - использование кэша
    ```
- О настройке почты smtp: 
[Настройка почтового сервиса SMTP ](https://proghunter.ru/articles/setting-up-the-smtp-mail-service-for-yandex-in-django)

### Настройка БД

- примените миграции:
  ```text
  python manage.py migrate
  ```
  
- примените фикстуры:
  ```text
  python -Xutf8 manage.py loaddata fixtures/*.json
  ```
  
### Запуск проекта
- запустите проект и перейдите по адресу
  ```text
  python manage.py runserver
  http://127.0.0.1:8000
  ```

- Для запуска периодической рассылки используйте APScheduler. И он будет проверять доступные рассылки раз в 10секунд.
Откройте новую вкладку в терминале и введите команду
  ```text
  python manage.py runapscheduler
  ```

- Для единоразового запуска рассылки используйте команду
  ```text
  python manage.py start_mailing
  ```

### Описание работы сервиса

После запуска проекта нужно перейти на сайт и пройти регистрацию или авторизацию. 
Зачем выбираем ссылку клиенты и заполняем их, далее выбираем ссылку сообщения и заполняем сообщение для рассылки 
и наконец переходим по ссылке рассылки и там настраиваем рассылку. После запуска рассылки сообщения отправляются всем вашим клиентам.
Вы можете посмотреть лог, перейдя в рассылку и нажав кнопку посмотреть лог.


