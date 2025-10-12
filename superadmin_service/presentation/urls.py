from django.urls import path

from presentation.views.auth_views import superadmin_login, superadmin_logout
from presentation.views.health_views import health_check

urlpatterns = [
    path("health/", health_check, name="health_check"),
    path("auth/login/", superadmin_login, name="superadmin_login"),
    path("auth/logout/", superadmin_logout, name="superadmin_logout"),
]
