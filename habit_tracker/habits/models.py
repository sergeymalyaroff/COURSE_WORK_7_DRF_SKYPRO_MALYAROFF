#COURSE_WORK_&_DRF_SKYPRO_MALYAROFF/habit_tracker/habits/models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.CharField(max_length=100)
    time = models.TimeField()
    action = models.CharField(max_length=200)
    is_nice_habit = models.BooleanField()
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    frequency = models.PositiveIntegerField(default=1)
    reward = models.CharField(max_length=200, null=True, blank=True)
    time_required = models.PositiveIntegerField()
    is_public = models.BooleanField(default=False)

    def clean(self):
        # Исключение одновременного выбора связанной привычки и указания вознаграждения
        if self.related_habit and self.reward:
            raise ValidationError(_('Cannot have both a related habit and a reward.'))

        # Время выполнения не больше 120 секунд
        if self.time_required > 120:
            raise ValidationError(_('Execution time must not exceed 120 seconds.'))

        # Связанные привычки могут быть только приятными
        if self.related_habit and not self.related_habit.is_nice_habit:
            raise ValidationError(_('Related habit must be a nice habit.'))

        # У приятной привычки не может быть вознаграждения или связанной привычки
        if self.is_nice_habit and (self.reward or self.related_habit):
            raise ValidationError(_('A nice habit cannot have a reward or a related habit.'))

        # Нельзя выполнять привычку реже, чем 1 раз в 7 дней
        if self.frequency > 7:
            raise ValidationError(_('The habit cannot be performed less frequently than once every 7 days.'))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.action
