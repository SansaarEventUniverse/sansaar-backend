from django.urls import path
from presentation.views.health_views import health_check
from presentation.views.event_role_views import (
    assign_event_role,
    revoke_event_role,
    check_event_permission
)

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('events/<str:event_id>/assign/', assign_event_role, name='assign_event_role'),
    path('events/<str:event_id>/revoke/', revoke_event_role, name='revoke_event_role'),
    path('events/<str:event_id>/check/', check_event_permission, name='check_event_permission'),
]
