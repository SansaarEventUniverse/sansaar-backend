from django.urls import path

from .views.auth_views import google_callback, login, register, resend_verification, verify_email
from .views.health_views import health_check

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('verify-email/<str:token>/', verify_email, name='verify_email'),
    path('resend-verification/', resend_verification, name='resend_verification'),
    path('google/callback/', google_callback, name='google_callback'),
]
