from django.contrib import admin
from django.urls import path

from account import views

urlpatterns = [
    path('register/', views.RegisterAPI.as_view())
]
