from django.contrib import admin
from django.urls import path

from presentation.views.health import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/events/health/', health_check, name='health_check'),
]
