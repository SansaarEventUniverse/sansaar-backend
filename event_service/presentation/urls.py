from django.urls import path

from presentation.views.health import health_check
from presentation.views.event_views import (
    create_event,
    get_event,
    update_event,
    save_draft,
    get_draft,
)
from presentation.views.event_status_views import (
    publish_event,
    unpublish_event,
    cancel_event,
    complete_event,
)

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('drafts/get/', get_draft, name='get_draft'),
    path('drafts/', save_draft, name='save_draft'),
    path('<str:event_id>/publish/', publish_event, name='publish_event'),
    path('<str:event_id>/unpublish/', unpublish_event, name='unpublish_event'),
    path('<str:event_id>/cancel/', cancel_event, name='cancel_event'),
    path('<str:event_id>/complete/', complete_event, name='complete_event'),
    path('<str:event_id>/update/', update_event, name='update_event'),
    path('<str:event_id>/', get_event, name='get_event'),
    path('', create_event, name='create_event'),
]
