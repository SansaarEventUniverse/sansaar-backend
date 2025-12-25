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
from presentation.views.system_health_views import (
    GetSystemHealthView,
    HealthCheckView,
    MonitoringDashboardView,
)
from presentation.views.api_analytics_views import (
    GetAPIAnalyticsView,
    APIUsageReportView,
    APIMonitoringView,
)

urlpatterns = [
    # Health Check
    path("health/", health_check, name="health_check"),
    
    # Authentication
    path("auth/login/", superadmin_login, name="superadmin_login"),
    path("auth/logout/", superadmin_logout, name="superadmin_logout"),
    
    # User Management
    path("users/", list_users, name="list_users"),
    path("users/<str:user_id>/", view_user, name="view_user"),
    path("users/<str:user_id>/deactivate/", deactivate_user, name="deactivate_user"),
    
    # Organization Management
    path("organizations/", list_organizations, name="list_organizations"),
    path("organizations/<str:org_id>/", view_organization, name="view_organization"),
    path(
        "organizations/<str:org_id>/delete/",
        delete_organization,
        name="delete_organization",
    ),
    
    # Audit Logs
    path("audit-logs/", search_audit_logs, name="search_audit_logs"),
    path("audit-logs/report/", generate_report, name="generate_report"),
    
    # System Health Monitoring
    path("admin/system-health/", GetSystemHealthView.as_view(), name="system_health"),
    path("admin/health-check/", HealthCheckView.as_view(), name="health_check_api"),
    path("admin/monitoring/", MonitoringDashboardView.as_view(), name="monitoring_dashboard"),
    
    # API Analytics & Usage Monitoring
    path("admin/api-analytics/", GetAPIAnalyticsView.as_view(), name="api_analytics"),
    path("admin/api-usage/", APIUsageReportView.as_view(), name="api_usage"),
    path("admin/api-monitoring/", APIMonitoringView.as_view(), name="api_monitoring"),
]
