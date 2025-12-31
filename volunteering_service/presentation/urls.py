from django.urls import path
from presentation.views.health_views import health_check
from presentation.views.opportunity_views import create_opportunity, get_opportunities, manage_opportunity

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('opportunities/create/', create_opportunity, name='create_opportunity'),
    path('opportunities/', get_opportunities, name='get_opportunities'),
    path('opportunities/<int:opportunity_id>/', manage_opportunity, name='manage_opportunity'),
]
