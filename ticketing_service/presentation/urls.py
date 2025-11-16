from django.urls import path
from presentation.views.health import health_check
from presentation.views.ticket_type_views import (
    create_ticket_type,
    update_ticket_type,
    get_ticket_types,
)
from presentation.views.ticket_views import (
    validate_qr_code,
    check_in_ticket,
    get_ticket,
)

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('events/<str:event_id>/ticket-types/', create_ticket_type, name='create_ticket_type'),
    path('events/<str:event_id>/ticket-types/list/', get_ticket_types, name='get_ticket_types'),
    path('ticket-types/<str:ticket_type_id>/', update_ticket_type, name='update_ticket_type'),
    path('tickets/validate/', validate_qr_code, name='validate_qr_code'),
    path('tickets/<str:ticket_id>/checkin/', check_in_ticket, name='check_in_ticket'),
    path('tickets/<str:ticket_id>/', get_ticket, name='get_ticket'),
]
