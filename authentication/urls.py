from allauth.account.views import LogoutView
from django.urls import path, include
from django.views.generic import TemplateView

from . import views
# from .views import GoogleLogin

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('verify-email/', views.VerifyEmail.as_view(), name='email-verify'),

    # path("", TemplateView.as_view(template_name="index.html")),
    # path('accounts/', include('allauth.urls')),
    # path("logout", LogoutView.as_view()),

    path('request-reset-email/', views.RequestPasswordResetEmailView.as_view(), name='request-reset-email'),
    path('password-reset-confirm/<uidb64>/<token>/', views.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', views.SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
]
