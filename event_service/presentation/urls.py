from django.urls import path

from presentation.views.health import health_check

urlpatterns = [
    path('api/events/health/', health_check, name='health_check'),
]
