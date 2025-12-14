from django.urls import path
from presentation.views.health import health_check
from presentation.views.analytics_views import get_analytics, get_realtime_metrics, analytics_query, create_analytics_event
from presentation.views.dashboard_views import get_dashboard, customize_dashboard, get_dashboard_widgets, create_dashboard
from presentation.views.event_analytics_views import (
    TrackViewAPI, TrackRegistrationAPI, EventMetricsAPI, CheckInAPI, CheckOutAPI, MetricsExportAPI, MetricsExportCSVAPI
)
from presentation.views.financial_views import (
    GetFinancialReportView, RevenueAnalyticsView, ExportFinancialView, ExportFinancialCSVView
)

urlpatterns = [
    # Health Check
    path('health/', health_check, name='health_check'),
    
    # Analytics Endpoints
    path('', get_analytics, name='get_analytics'),
    path('real-time/', get_realtime_metrics, name='realtime_metrics'),
    path('query/', analytics_query, name='analytics_query'),
    path('events/', create_analytics_event, name='create_event'),
    
    # Event Analytics Endpoints
    path('events/<str:event_id>/track-view/', TrackViewAPI.as_view(), name='track_view'),
    path('events/<str:event_id>/track-registration/', TrackRegistrationAPI.as_view(), name='track_registration'),
    path('events/<str:event_id>/metrics/', EventMetricsAPI.as_view(), name='event_metrics'),
    path('events/<str:event_id>/check-in/', CheckInAPI.as_view(), name='check_in'),
    path('events/<str:event_id>/check-out/', CheckOutAPI.as_view(), name='check_out'),
    path('events/<str:event_id>/export-csv/', MetricsExportCSVAPI.as_view(), name='metrics_export_csv'),
    path('events/<str:event_id>/export/', MetricsExportAPI.as_view(), name='metrics_export'),
    
    # Financial Reporting Endpoints
    path('events/<str:event_id>/financial/', GetFinancialReportView.as_view(), name='financial_report'),
    path('events/<str:event_id>/revenue-analytics/', RevenueAnalyticsView.as_view(), name='revenue_analytics'),
    path('events/<str:event_id>/financial/export/', ExportFinancialView.as_view(), name='financial_export'),
    path('events/<str:event_id>/financial/export-csv/', ExportFinancialCSVView.as_view(), name='financial_export_csv'),
    
    # Dashboard Endpoints
    path('organizer/dashboard/', create_dashboard, name='create_dashboard'),
    path('organizer/dashboard/<int:dashboard_id>/', get_dashboard, name='get_dashboard'),
    path('organizer/dashboard/<int:dashboard_id>/customize/', customize_dashboard, name='customize_dashboard'),
    path('organizer/dashboard/<int:dashboard_id>/widgets/', get_dashboard_widgets, name='get_dashboard_widgets'),
]
