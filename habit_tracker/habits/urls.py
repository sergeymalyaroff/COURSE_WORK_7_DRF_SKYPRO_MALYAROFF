# COURSE_WORK_&_DRF_SKYPRO_MALYAROFF/habit_tracker/habits/urls.py

from django.urls import path, re_path
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Настройка schema_view для drf-yasg
schema_view = get_schema_view(
   openapi.Info(
      title="Habit Tracker API",
      default_version='v1',
      description="API documentation for Habit Tracker",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("create/", views.create_habit, name="create_habit"),
    path("edit/<int:habit_id>/", views.edit_habit, name="edit_habit"),
    path("delete/<int:habit_id>/", views.delete_habit, name="delete_habit"),
    path("get_habits/", views.get_habits, name="get_habits"),
    path("get_public_habits/", views.get_public_habits,
         name="get_public_habits"),
    path("register/", views.register, name="register"),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui"
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc"
    ),
]
