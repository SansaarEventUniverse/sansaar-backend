from django.urls import path

from presentation.views.health import health_check
from presentation.views.venue_views import (
    create_venue,
    get_venue,
    update_venue,
    search_venues,
)

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('search/', search_venues, name='search_venues'),
    path('<str:venue_id>/', get_venue, name='get_venue'),
    path('<str:venue_id>/update/', update_venue, name='update_venue'),
    path('', create_venue, name='create_venue'),
]
