from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_habit, name='create_habit'),
    path('edit/<int:habit_id>/', views.edit_habit, name='edit_habit'),
    path('delete/<int:habit_id>/', views.delete_habit, name='delete_habit'),
    path('get_habits/', views.get_habits, name='get_habits'),
    path('get_public_habits/', views.get_public_habits, name='get_public_habits'),
    path('register/', views.register, name='register'),
]



