from django.urls import path

from .views.health_views import health_check
from .views.profile_views import (
    delete_address,
    delete_phone,
    delete_profile_picture,
    get_profile,
    update_profile,
    upload_profile_picture,
)

urlpatterns = [
    path("health/", health_check, name="health_check"),
    path("profile/<str:user_id>/", get_profile, name="get_profile"),
    path("profile/<str:user_id>/update/", update_profile, name="update_profile"),
    path("profile/<str:user_id>/picture/", upload_profile_picture, name="upload_profile_picture"),
    path("profile/<str:user_id>/phone/", delete_phone, name="delete_phone"),
    path("profile/<str:user_id>/address/", delete_address, name="delete_address"),
    path("profile/<str:user_id>/picture/delete/", delete_profile_picture, name="delete_profile_picture"),
]
