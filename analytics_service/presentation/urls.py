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
from presentation.views.user_views import UserAnalyticsAPI, UserActivityAPI, UsersListAPI
from presentation.views.visualization_views import (
    GetVisualizationView, CreateVisualizationView, CreateChartView, ExportChartView
)
from presentation.views.report_views import BuildReportView, SaveTemplateView, GenerateReportView
from presentation.views.performance_views import GetPerformanceView, SystemHealthView, AlertsView
from presentation.views.export_views import ExportDataView, ScheduleExportView, GetExportStatusView
from presentation.views.audit_views import GetAuditTrailView, ComplianceReportView, AuditSearchView
from presentation.views.mobile_dashboard_views import GetMobileDashboardView, MobileWidgetsView
from presentation.views.feedback_views import submit_feedback, get_feedback, feedback_analytics

urlpatterns = [
    # Health Check
    path('health/', health_check, name='health_check'),
    
    # Analytics Endpoints
    path('', get_analytics, name='get_analytics'),
    path('real-time/', get_realtime_metrics, name='realtime_metrics'),
    path('query/', analytics_query, name='analytics_query'),
    path('events/', create_analytics_event, name='create_event'),
    
    # Event Feedback
    path('events/<int:event_id>/feedback/', submit_feedback, name='submit_feedback'),
    path('events/<int:event_id>/feedback/list/', get_feedback, name='get_feedback'),
    path('events/<int:event_id>/feedback/analytics/', feedback_analytics, name='feedback_analytics'),
    
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
    
    # User Management Endpoints
    path('admin/user-analytics/', UserAnalyticsAPI.as_view(), name='user_analytics'),
    path('admin/user-activity/', UserActivityAPI.as_view(), name='user_activity'),
    path('admin/users/', UsersListAPI.as_view(), name='users_list'),
    
    # Visualization Endpoints
    path('visualizations/<int:visualization_id>/', GetVisualizationView.as_view(), name='get_visualization'),
    path('visualizations/', CreateVisualizationView.as_view(), name='create_visualization'),
    path('charts/', CreateChartView.as_view(), name='create_chart'),
    path('charts/<int:chart_id>/export/', ExportChartView.as_view(), name='export_chart'),
    
    # Report Builder Endpoints
    path('reports/build/', BuildReportView.as_view(), name='build_report'),
    path('report-templates/', SaveTemplateView.as_view(), name='save_template'),
    path('reports/generate/', GenerateReportView.as_view(), name='generate_report'),
    
    # Performance Monitoring Endpoints
    path('admin/performance/', GetPerformanceView.as_view(), name='get_performance'),
    path('admin/system-health/', SystemHealthView.as_view(), name='system_health'),
    path('admin/alerts/', AlertsView.as_view(), name='alerts'),
    
    # Data Export Endpoints
    path('data/export/', ExportDataView.as_view(), name='export_data'),
    path('data/schedule-export/', ScheduleExportView.as_view(), name='schedule_export'),
    path('exports/<int:export_id>/status/', GetExportStatusView.as_view(), name='export_status'),
    
    # Audit Trail Endpoints
    path('admin/audit-trail/', GetAuditTrailView.as_view(), name='audit_trail'),
    path('admin/compliance/', ComplianceReportView.as_view(), name='compliance_report'),
    path('admin/audit/search/', AuditSearchView.as_view(), name='audit_search'),
    
    # Mobile Dashboard Endpoints
    path('mobile/dashboard/<int:dashboard_id>/', GetMobileDashboardView.as_view(), name='mobile_dashboard'),
    path('mobile/widgets/', MobileWidgetsView.as_view(), name='mobile_widgets'),
]
