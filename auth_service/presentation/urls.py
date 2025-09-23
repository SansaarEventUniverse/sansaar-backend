from django.urls import path

from .views.auth_views import (
    google_callback,
    login,
    register,
    request_password_reset,
    resend_verification,
    reset_password,
    verify_email,
)
from .views.health_views import health_check

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('verify-email/<str:token>/', verify_email, name='verify_email'),
    path('resend-verification/', resend_verification, name='resend_verification'),
    path('password-reset/request/', request_password_reset, name='request_password_reset'),
    path('password-reset/confirm/', reset_password, name='reset_password'),
    path('google/callback/', google_callback, name='google_callback'),
]
