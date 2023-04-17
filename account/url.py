from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from account import views

urlpatterns = [
    path('register/', views.RegisterAPI.as_view()),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('addaccount/', views.AddAccountApi.as_view(), name='login'),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="RefreshToken"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="RefreshToken"),
]
