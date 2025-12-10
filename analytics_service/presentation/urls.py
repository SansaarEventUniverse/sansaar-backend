from django.urls import path
from presentation.views.health import health_check
from presentation.views.analytics_views import get_analytics, get_realtime_metrics, analytics_query, create_analytics_event

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('', get_analytics, name='get_analytics'),
    path('real-time/', get_realtime_metrics, name='realtime_metrics'),
    path('query/', analytics_query, name='analytics_query'),
    path('events/', create_analytics_event, name='create_event'),
]
