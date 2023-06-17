from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from rest_framework.routers import DefaultRouter
from account import views



router=DefaultRouter()
router.register('files',views.MarksheetApi, basename='files')


urlpatterns = [
    path('register', views.RegisterAPI.as_view()),
    path('login', views.LoginAPI.as_view(), name='login'),
    path('SentMailView', views.SentMailView.as_view(), name="sentmail"),
    path('ResetPasswordview', views.ResetPasswordview.as_view()),
    path('otp', views.OtpVerification.as_view()),
    path('addaccount', views.AddAccountApi.as_view(), name='addaccount'),
    path('payrollelement', views.PayrollElementView.as_view(), name='payrollelement'),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="RefreshToken"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="RefreshToken"),
    path('financeout', views.FinanceOutAPI.as_view(), name='financeout'),
    path('Month_Finance_out', views.Month_Finance_outApi.as_view(), name='Month_Finance_out'),
    path('financein', views.FinanceInApi.as_view(), name='financein'),
    path('bill', views.BillApiView.as_view(), name='addition'),
    path('payment', views.PaymentApiView.as_view(), name='payment'),
    path('invoice', views.InvoiceApiView.as_view(), name='invoice'),
    path('vendor', views.VendorApiView.as_view(),name='vendor'),
    path('payroll', views.PayrollAPI.as_view(), name='payroll'),
    path('marksheet', views.MarksheetApi.as_view({'get':'list','post':'create'}), name='marksheet'),
    path('evaluation', views.EvaluationAPI.as_view(), name='evaluation'),
    path ('api', include(router.urls)),
    path('exportin', views.Finance_in_ExcelExport.as_view(), name='export'),
    path('exportout', views.Finance_Out_ExcelExport.as_view(), name='export'),
    path('upload', views.Finance_In_FileUploadView.as_view(), name='upload'),
    path('Financetotal', views.Financetotal.as_view(), name='Financetotal'),
    ] 