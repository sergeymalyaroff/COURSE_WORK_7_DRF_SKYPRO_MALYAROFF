# COURSE_WORK_&_DRF_SKYPRO_MALYAROFF/habit_tracker/celery_config.py

import os
from celery import Celery

# Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "habit_tracker.settings")

# Создаем экземпляр Celery
app = Celery("habit_tracker")

# Загружаем настройки из Django
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически загружаем задачи из всех файлов tasks.py в приложениях Django
app.autodiscover_tasks()
