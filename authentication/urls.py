from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('verify-email/', views.VerifyEmail.as_view(), name='email-verify'),

    path('request-reset-email/', views.RequestPasswordResetEmailView.as_view(), name='request-reset-email'),
    path('password-reset-confirm/<uidb64>/<token>/', views.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', views.SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
]
