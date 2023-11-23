#COURSE_WORK_&_DRF_SKYPRO_MALYAROFF/habit_tracker/habits/views.py

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
@require_POST
def register(request):
    # Парсинг данных из JSON-запроса
    data = json.loads(request.body)

    username = data.get('username')
    password = data.get('password')

    # Проверка, что обязательные поля были переданы
    if not username or not password:
        return JsonResponse({'error': 'Both username and password are required'})

    # Проверка, что пользователь с таким именем не существует
    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'})

    # Создание нового пользователя
    user = User.objects.create_user(username=username, password=password)

    # Аутентификация пользователя
    user = authenticate(request, username=username, password=password)

    if user is not None:
        # Авторизация пользователя
        login(request, user)
        return JsonResponse({'message': 'Registration successful'})
    else:
        return JsonResponse({'error': 'Registration failed'})


from .models import Habit

# Эндпоинт для создания новой привычки
@login_required
@require_http_methods(["POST"])
def create_habit(request):
    # Проверка, что запрос является POST-запросом
    if request.method == 'POST':
        # Получение данных из POST-запроса
        data = request.POST

        # Извлечение необходимых данных из запроса
        user = request.user
        action = data.get('action')
        time = data.get('time')
        place = data.get('place')
        is_pleasurable = data.get('is_pleasurable')
        is_public = data.get('is_public')
        related_habit_id = data.get('related_habit_id')
        reward = data.get('reward')
        estimated_time = data.get('estimated_time')

        # Создание новой привычки в базе данных
        habit = Habit.objects.create(
            user=user,
            action=action,
            time=time,
            place=place,
            is_pleasurable=is_pleasurable,
            is_public=is_public,
            related_habit_id=related_habit_id,
            reward=reward,
            estimated_time=estimated_time
        )

        # Возвращение JSON-ответа с информацией о созданной привычке
        return JsonResponse({'message': 'Habit created successfully', 'habit_id': habit.id})
    else:
        # Возвращение ошибки, если запрос не является POST-запросом
        return JsonResponse({'error': 'Only POST requests are allowed'})

# Эндпоинт для редактирования существующей привычки
@login_required
@require_http_methods(["PUT"])
def edit_habit(request, habit_id):
    # Проверка, что запрос является PUT-запросом
    if request.method == 'PUT':
        # Получение привычки по ее ID или возврат ошибки, если привычка не найдена
        habit = get_object_or_404(Habit, id=habit_id)

        # Проверка, что пользователь, выполняющий запрос, является владельцем привычки
        if habit.user == request.user:
            # Получение данных из PUT-запроса
            data = request.POST

            # Обновление данных привычки
            habit.action = data.get('action', habit.action)
            habit.time = data.get('time', habit.time)
            habit.place = data.get('place', habit.place)
            habit.is_pleasurable = data.get('is_pleasurable', habit.is_pleasurable)
            habit.is_public = data.get('is_public', habit.is_public)
            habit.related_habit_id = data.get('related_habit_id', habit.related_habit_id)
            habit.reward = data.get('reward', habit.reward)
            habit.estimated_time = data.get('estimated_time', habit.estimated_time)

            # Сохранение обновленных данных в базе данных
            habit.save()

            # Возвращение JSON-ответа с информацией о обновленной привычке
            return JsonResponse({'message': 'Habit updated successfully'})
        else:
            # Возвращение ошибки, если пользователь не является владельцем привычки
            return JsonResponse({'error': 'You do not have permission to edit this habit'})
    else:
        # Возвращение ошибки, если запрос не является PUT-запросом
        return JsonResponse({'error': 'Only PUT requests are allowed'})

# Эндпоинт для удаления привычки
@login_required
@require_http_methods(["DELETE"])
def delete_habit(request, habit_id):
    # Проверка, что запрос является DELETE-запросом
    if request.method == 'DELETE':
        # Получение привычки по ее ID или возврат ошибки, если привычка не найдена
        habit = get_object_or_404(Habit, id=habit_id)

        # Проверка, что пользователь, выполняющий запрос, является владельцем привычки
        if habit.user == request.user:
            # Удаление привычки из базы данных
            habit.delete()

            # Возвращение JSON-ответа с сообщением об успешном удалении
            return JsonResponse({'message': 'Habit deleted successfully'})
        else:
            # Возвращение ошибки, если пользователь не является владельцем привычки
            return JsonResponse({'error': 'You do not have permission to delete this habit'})
    else:
        # Возвращение ошибки, если запрос не является DELETE-запросом
        return JsonResponse({'error': 'Only DELETE requests are allowed'})

# Эндпоинт для получения списка привычек текущего пользователя с пагинацией
@login_required
@require_http_methods(["GET"])
def get_habits(request):
    # Проверка, что запрос является GET-запросом
    if request.method == 'GET':
        # Получение списка привычек текущего пользователя с пагина
