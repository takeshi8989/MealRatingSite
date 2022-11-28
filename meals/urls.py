from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='landing'),
    path('detail_<int:mealId>/', views.detail, name='detail'),
    path('logout/', views.log_out, name='logout'),
    path('home/tags_<str:tags>/sort_<str:sortBy>/', views.category, name='home'),
    path('register/', views.register, name='register'),
    path('add_meal/', views.addMeal, name='add_meal'),
    path('history/', views.history, name='history')
]
