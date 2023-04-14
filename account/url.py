from django.contrib import admin
from django.urls import path

from account import views

urlpatterns = [
    path('index/',views.index.as_views())
]