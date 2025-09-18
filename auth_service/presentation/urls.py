from django.urls import path
from .views.health_views import health_check
from .views.auth_views import register

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('register/', register, name='register'),
]
