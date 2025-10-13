from django.urls import path

from .views.health_views import health_check
from .views.organization_views import delete_organization, get_organization, list_organizations
from .views.profile_views import get_profile, list_profiles, update_profile, upload_profile_picture

urlpatterns = [
    path("health/", health_check, name="health_check"),
    path("profiles/", list_profiles, name="list_profiles"),
    path("profile/<str:user_id>/", get_profile, name="get_profile"),
    path("profile/<str:user_id>/update/", update_profile, name="update_profile"),
    path("profile/<str:user_id>/picture/", upload_profile_picture, name="upload_profile_picture"),
    path("organizations/", list_organizations, name="list_organizations"),
    path("organization/<str:org_id>/", get_organization, name="get_organization"),
    path("organization/<str:org_id>/delete/", delete_organization, name="delete_organization"),
]
