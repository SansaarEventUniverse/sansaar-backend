from django.urls import path

from presentation.views.health import health_check
from presentation.views.registration_views import (
    register_for_event,
    cancel_registration,
    get_event_registrations,
    check_capacity,
)
from presentation.views.waitlist_views import (
    join_waitlist,
    leave_waitlist,
    get_waitlist_position,
    get_event_waitlist,
)

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('events/<str:event_id>/register/', register_for_event, name='register_for_event'),
    path('events/<str:event_id>/cancel/', cancel_registration, name='cancel_registration'),
    path('events/<str:event_id>/', get_event_registrations, name='get_event_registrations'),
    path('events/<str:event_id>/capacity/', check_capacity, name='check_capacity'),
    path('events/<str:event_id>/waitlist/', join_waitlist, name='join_waitlist'),
    path('events/<str:event_id>/waitlist/leave/', leave_waitlist, name='leave_waitlist'),
    path('events/<str:event_id>/waitlist/position/', get_waitlist_position, name='get_waitlist_position'),
    path('events/<str:event_id>/waitlist/list/', get_event_waitlist, name='get_event_waitlist'),
]
