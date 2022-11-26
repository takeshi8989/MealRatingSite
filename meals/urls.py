from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/', views.category, name='category'),
    path('detail_<int:mealId>/', views.detail, name='detail'),
    path('logout', views.log_out, name='logout')
]
