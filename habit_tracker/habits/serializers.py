# habits.serialisers.py

# habits/serializers.py

from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_nice_habit",
            "related_habit",
            "frequency",
            "reward",
            "time_required",
            "is_public",
        ]
        # Добавьте или уберите поля в зависимости от того, какие данные ваша
        # модель содержит и что вы хотите сериализовать
