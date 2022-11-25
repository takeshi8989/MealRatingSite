from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<str:categoryName>_<str:sortBy>/', views.category, name='category'),
    path('detail_<int:mealId>/', views.detail, name='detail')
]
