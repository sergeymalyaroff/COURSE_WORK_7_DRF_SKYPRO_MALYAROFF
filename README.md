**Habit Tracker**

Проект "Habit Tracker" – это веб-приложение для отслеживания личных привычек. Это помогает пользователям устанавливать, следить и поддерживать здоровые привычки.

Начало работы

Эти инструкции помогут вам запустить проект локально на вашем компьютере для разработки и тестирования.

Предварительные требования
Что вам нужно для установки:

Python (3.8 или выше)
Django (4.2.7 или выше)
PostgreSQL
Celery (для асинхронных задач)
Установка
Клонируйте репозиторий и установите зависимости:


git clone https://github.com/sergeymalyaroff/COURSE_WORK_7_DRF_SKYPRO_MALYAROFF
cd habit-tracker
pip install -r requirements.txt


Настройка базы данных

Создайте базу данных PostgreSQL и настройте параметры в settings.py:


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'имя_базы_данных',
        'USER': 'имя_пользователя',
        'PASSWORD': 'пароль',
        'HOST': 'localhost',
        'PORT': '',
    }
}
Запустите миграции:


python manage.py migrate
Запуск проекта


python manage.py runserver

Использование

После запуска сервера Django, вы можете взаимодействовать с API через эндпоинты, определенные в habits/urls.py.

Документация API

Для доступа к документации API перейдите по ссылке: http://localhost:8000/swagger/

Тестирование

Запустите тесты, чтобы убедиться в корректности работы:


python manage.py test

Развертывание

Для развертывания в продакшн используйте соответствующие инструменты и сервисы, такие как Heroku, AWS или Docker.

Сделано с использованием

Django - Веб-фреймворк
PostgreSQL - Система управления базами данных
DRF - Django REST framework
Celery - Для асинхронных задач
