# COURSE_WORK_&_DRF_SKYPRO_MALYAROFF/habit_tracker/habits/views.py

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
import json
from .models import Habit, UserProfile
from .serializers import HabitSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .tasks import send_habit_notification


@csrf_exempt
@require_POST
def register(request):
    """
    Регистрация нового пользователя.
    Парсит данные из JSON-запроса и создает нового пользователя.
    """
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return JsonResponse({"error": "Both username and password are required"})

    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists"})

    user = User.objects.create_user(username=username, password=password)
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({"message": "Registration successful"})
    else:
        return JsonResponse({"error": "Registration failed"})


@login_required
@require_http_methods(["POST"])
def create_habit(request):
    """
    Создание новой привычки.
    Получает данные из POST-запроса и создает новую привычку для пользователя.
    """
    data = request.POST
    user = request.user
    action = data.get("action")
    time = data.get("time")
    place = data.get("place")
    is_pleasurable = data.get("is_pleasurable")
    is_public = data.get("is_public")
    related_habit_id = data.get("related_habit_id")
    reward = data.get("reward")
    estimated_time = data.get("estimated_time")

    habit = Habit.objects.create(
        user=user,
        action=action,
        time=time,
        place=place,
        is_pleasurable=is_pleasurable,
        is_public=is_public,
        related_habit_id=related_habit_id,
        reward=reward,
        estimated_time=estimated_time,
    )

    user_profile = UserProfile.objects.get(user=user)
    if user_profile.telegram_chat_id:
        send_habit_notification.delay(
            user_profile.telegram_chat_id, f"Создана новая привычка: {action}"
        )

    return JsonResponse({"message": "Habit created successfully", "habit_id": habit.id})


@login_required
@require_http_methods(["PUT"])
def edit_habit(request, habit_id):
    """
    Редактирование существующей привычки.
    Обновляет данные привычки, если пользователь имеет к ней доступ.
    """
    habit = get_object_or_404(Habit, id=habit_id)
    if habit.user == request.user:
        data = request.POST
        habit.action = data.get("action", habit.action)
        habit.time = data.get("time", habit.time)
        habit.place = data.get("place", habit.place)
        habit.is_pleasurable = data.get("is_pleasurable", habit.is_pleasurable)
        habit.is_public = data.get("is_public", habit.is_public)
        habit.related_habit_id = data.get("related_habit_id", habit.related_habit_id)
        habit.reward = data.get("reward", habit.reward)
        habit.estimated_time = data.get("estimated_time", habit.estimated_time)
        habit.save()

        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.telegram_chat_id:
            send_habit_notification.delay(
                user_profile.telegram_chat_id, f"Привычка обновлена: {habit.action}"
            )

        return JsonResponse({"message": "Habit updated successfully"})
    else:
        return JsonResponse({"error": "You do not have permission to edit this habit"})


@login_required
@require_http_methods(["DELETE"])
def delete_habit(request, habit_id):
    """
    Удаление привычки.
    Удаляет привычку, если пользователь имеет к ней доступ.
    """
    habit = get_object_or_404(Habit, id=habit_id)
    if habit.user == request.user:
        habit.delete()

        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.telegram_chat_id:
            send_habit_notification.delay(
                user_profile.telegram_chat_id, f"Привычка удалена: {habit.action}"
            )

        return JsonResponse({"message": "Habit deleted successfully"})
    else:
        return JsonResponse(
            {"error": "You do not have permission to delete this habit"}
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_public_habits(request):
    """
    Получение списка публичных привычек.
    Возвращает список всех публичных привычек для аутентифицированных пользователей.
    """
    habits = Habit.objects.filter(is_public=True)
    serializer = HabitSerializer(habits, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_habits(request):
    """
    Получение списка привычек пользователя.
    Возвращает список привычек, созданных аутентифицированным пользователем, с пагинацией.
    """
    habits = Habit.objects.filter(user=request.user)
    paginator = PageNumberPagination()
    page = paginator.paginate_queryset(habits, request)
    if page is not None:
        serializer = HabitSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    serializer = HabitSerializer(habits, many=True)
    return Response(serializer.data)
