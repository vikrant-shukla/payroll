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
    path('financeout/', views.FinanceOutAPI.as_view(), name='financeout'),
    path('financein/', views.FinanceInApi.as_view(), name='financein'),
    path('bill/', views.BillApiView.as_view(), name='bill'),
    path('payment/', views.PaymentApiView.as_view(), name='payment'),
    path('invoice/', views.InvoiceApiView.as_view(), name='invoice'),
    path('payroll/', views.PayrollAPI.as_view(), name='payroll'),
    path('marksheet/', views.MarksheetApi.as_view(), name='marksheet'),
    path('garduationmarksheet/', views.Graduation_detailsApi.as_view(), name='garduationmarksheet'),
    path('Postgarduationmarksheet/', views.PostGraduationApi.as_view(), name='Postgarduationmarksheet'),
    path('evaluation/', views.EvaluationAPI.as_view(), name='evaluation'),
    path('insuarance/', views.InsuranceAPI.as_view(), name='insuarance'),





]
