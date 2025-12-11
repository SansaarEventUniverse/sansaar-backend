from django.urls import path
from presentation.views.health import health_check
from presentation.views.analytics_views import get_analytics, get_realtime_metrics, analytics_query, create_analytics_event
from presentation.views.dashboard_views import get_dashboard, customize_dashboard, get_dashboard_widgets, create_dashboard

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('', get_analytics, name='get_analytics'),
    path('real-time/', get_realtime_metrics, name='realtime_metrics'),
    path('query/', analytics_query, name='analytics_query'),
    path('events/', create_analytics_event, name='create_event'),
    path('organizer/dashboard/', create_dashboard, name='create_dashboard'),
    path('organizer/dashboard/<int:dashboard_id>/', get_dashboard, name='get_dashboard'),
    path('organizer/dashboard/<int:dashboard_id>/customize/', customize_dashboard, name='customize_dashboard'),
    path('organizer/dashboard/<int:dashboard_id>/widgets/', get_dashboard_widgets, name='get_dashboard_widgets'),
]
