from django.urls import path
from presentation.views.health import health_check
from presentation.views.ticket_type_views import (
    create_ticket_type,
    update_ticket_type,
    get_ticket_types,
)

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('events/<str:event_id>/ticket-types/', create_ticket_type, name='create_ticket_type'),
    path('events/<str:event_id>/ticket-types/list/', get_ticket_types, name='get_ticket_types'),
    path('ticket-types/<str:ticket_type_id>/', update_ticket_type, name='update_ticket_type'),
]
