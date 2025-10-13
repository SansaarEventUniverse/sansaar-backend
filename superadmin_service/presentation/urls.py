from django.urls import path

from presentation.views.auth_views import superadmin_login, superadmin_logout
from presentation.views.health_views import health_check
from presentation.views.user_views import deactivate_user, list_users, view_user

urlpatterns = [
    path("health/", health_check, name="health_check"),
    path("auth/login/", superadmin_login, name="superadmin_login"),
    path("auth/logout/", superadmin_logout, name="superadmin_logout"),
    path("users/", list_users, name="list_users"),
    path("users/<str:user_id>/", view_user, name="view_user"),
    path("users/<str:user_id>/deactivate/", deactivate_user, name="deactivate_user"),
]
