# habits.tests.py

from django.contrib.auth.models import User
from django.test import TestCase
from .models import Habit
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

class ModelTestCase(TestCase):
    """Тесты для моделей приложения habits."""

    def setUp(self):
        """Настройка тестового окружения."""
        user = User.objects.create(username="testuser", password="testpassword")
        self.habit_action = "Утренняя пробежка"
        self.habit = Habit(user=user, action=self.habit_action, time="07:00:00",
                           place="Парк", is_nice_habit=True, frequency=1, time_required=10, is_public=True)

    def test_model_can_create_a_habit(self):
        """Тест на создание новой привычки."""
        old_count = Habit.objects.count()
        self.habit.save()
        new_count = Habit.objects.count()
        self.assertNotEqual(old_count, new_count)

class ViewTestCase(TestCase):
    """Тесты для API эндпоинтов приложения habits."""

    def setUp(self):
        """Настройка клиента API и пользователя."""
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)
        self.habit_data = {'user': self.user.id, 'action': 'Утренняя йога', 'time': '06:00:00', 'place': 'Дом', 'is_nice_habit': True, 'frequency': 1, 'time_required': 15, 'is_public': True}
        self.response = self.client.post(
            reverse('create_habit'),
            self.habit_data,
            format="json")

    def test_api_can_create_a_habit(self):
        """Тест на создание привычки через API."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_authorization_is_enforced(self):
        """Тест на проверку авторизации."""
        new_client = APIClient()
        res = new_client.get('/habits/', kwargs={'pk': 3}, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_can_get_a_habit(self):
        """Тест на получение привычки через API."""
        habit = Habit.objects.get(id=1)
        response = self.client.get(
            '/habits/',
            kwargs={'pk': habit.id}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, habit)

    def test_api_can_update_habit(self):
        """Тест на обновление привычки через API."""
        habit = Habit.objects.get()
        change_habit = {'action': 'Вечерняя пробежка'}
        res = self.client.put(
            reverse('details', kwargs={'pk': habit.id}),
            change_habit, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_habit(self):
        """Тест на удаление привычки через API."""
        habit = Habit.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'pk': habit.id}),
            format='json',
            follow=True)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)



