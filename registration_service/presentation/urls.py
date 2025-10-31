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
from presentation.views.capacity_views import (
    get_capacity,
    create_capacity_rule,
)
from presentation.views.form_views import (
    create_form,
    get_form,
    submit_form,
)
from presentation.views.group_views import (
    create_group,
    join_group,
    get_group,
    confirm_group,
    cancel_group,
    get_group_stats,
)
from presentation.views.analytics_views import (
    get_analytics,
    get_dashboard,
    export_analytics,
)

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('events/<str:event_id>/register/', register_for_event, name='register_for_event'),
    path('events/<str:event_id>/cancel/', cancel_registration, name='cancel_registration'),
    path('events/<str:event_id>/', get_event_registrations, name='get_event_registrations'),
    path('events/<str:event_id>/capacity/', check_capacity, name='check_capacity'),
    path('events/<str:event_id>/capacity/info/', get_capacity, name='get_capacity'),
    path('events/<str:event_id>/capacity/rule/', create_capacity_rule, name='create_capacity_rule'),
    path('events/<str:event_id>/waitlist/', join_waitlist, name='join_waitlist'),
    path('events/<str:event_id>/waitlist/leave/', leave_waitlist, name='leave_waitlist'),
    path('events/<str:event_id>/waitlist/position/', get_waitlist_position, name='get_waitlist_position'),
    path('events/<str:event_id>/waitlist/list/', get_event_waitlist, name='get_event_waitlist'),
    path('events/<str:event_id>/form/', create_form, name='create_form'),
    path('events/<str:event_id>/form/get/', get_form, name='get_form'),
    path('events/<str:event_id>/form/submit/', submit_form, name='submit_form'),
    path('events/<str:event_id>/groups/stats/', get_group_stats, name='get_group_stats'),
    path('events/<str:event_id>/groups/', create_group, name='create_group'),
    path('events/<str:event_id>/groups/<str:group_id>/', get_group, name='get_group'),
    path('events/<str:event_id>/groups/<str:group_id>/join/', join_group, name='join_group'),
    path('events/<str:event_id>/groups/<str:group_id>/confirm/', confirm_group, name='confirm_group'),
    path('events/<str:event_id>/groups/<str:group_id>/cancel/', cancel_group, name='cancel_group'),
    path('events/<str:event_id>/analytics/', get_analytics, name='get_analytics'),
    path('events/<str:event_id>/analytics/dashboard/', get_dashboard, name='get_dashboard'),
    path('events/<str:event_id>/analytics/export/', export_analytics, name='export_analytics'),
]
