from django.db import models
from django.contrib.auth.models import User

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

    def __str__(self):
        return self.action
