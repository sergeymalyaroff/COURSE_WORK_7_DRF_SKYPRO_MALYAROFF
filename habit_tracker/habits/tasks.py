# habits.tasks.py

from celery import shared_task
from .models import Habit,
from .telegram_bot import send_habit_notification
from django.utils import timezone


@shared_task
def send_habit_notifications():
    """
    Отправляет уведомления пользователям о их привычках.
    """
    habits = Habit.objects.filter(next_notification_time__lte=timezone.now())
    for habit in habits:
        if habit.user.userprofile.telegram_chat_id:
            message = f"Не забудьте о привычке: {habit.name}"
            send_habit_notification(
                habit.user.userprofile.telegram_chat_id, message)
