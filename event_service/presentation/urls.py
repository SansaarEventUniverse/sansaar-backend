from django.urls import path

from presentation.views.health import health_check
from presentation.views.event_views import (
    create_event,
    get_event,
    update_event,
    save_draft,
    get_draft,
)

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('drafts/get/', get_draft, name='get_draft'),
    path('drafts/', save_draft, name='save_draft'),
    path('<str:event_id>/update/', update_event, name='update_event'),
    path('<str:event_id>/', get_event, name='get_event'),
    path('', create_event, name='create_event'),
]
