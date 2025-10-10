from django.urls import path

from presentation.views.health_views import health_check

urlpatterns = [
    path("health/", health_check, name="health_check"),
]
