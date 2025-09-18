from django.urls import path

from .views.auth_views import register
from .views.health_views import health_check

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('register/', register, name='register'),
]
