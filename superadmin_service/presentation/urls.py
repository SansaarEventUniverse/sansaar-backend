from django.urls import path

from presentation.views.audit_views import generate_report, search_audit_logs
from presentation.views.auth_views import superadmin_login, superadmin_logout
from presentation.views.health_views import health_check
from presentation.views.organization_views import (
    delete_organization,
    list_organizations,
    view_organization,
)
from presentation.views.user_views import deactivate_user, list_users, view_user

urlpatterns = [
    path("health/", health_check, name="health_check"),
    path("auth/login/", superadmin_login, name="superadmin_login"),
    path("auth/logout/", superadmin_logout, name="superadmin_logout"),
    path("users/", list_users, name="list_users"),
    path("users/<str:user_id>/", view_user, name="view_user"),
    path("users/<str:user_id>/deactivate/", deactivate_user, name="deactivate_user"),
    path("organizations/", list_organizations, name="list_organizations"),
    path("organizations/<str:org_id>/", view_organization, name="view_organization"),
    path(
        "organizations/<str:org_id>/delete/",
        delete_organization,
        name="delete_organization",
    ),
    path("audit-logs/", search_audit_logs, name="search_audit_logs"),
    path("audit-logs/report/", generate_report, name="generate_report"),
]
