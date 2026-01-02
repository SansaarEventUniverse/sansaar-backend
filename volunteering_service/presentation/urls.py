from django.urls import path
from presentation.views.health_views import health_check
from presentation.views.opportunity_views import create_opportunity, get_opportunities, manage_opportunity
from presentation.views.application_views import apply_for_opportunity, get_applications, manage_application

urlpatterns = [
    # Health Check
    path('health/', health_check, name='health_check'),
    
    # Volunteer Opportunities
    path('opportunities/create/', create_opportunity, name='create_opportunity'),
    path('opportunities/', get_opportunities, name='get_opportunities'),
    path('opportunities/<int:opportunity_id>/', manage_opportunity, name='manage_opportunity'),
    
    # Volunteer Applications
    path('opportunities/<int:opportunity_id>/apply/', apply_for_opportunity, name='apply_for_opportunity'),
    path('applications/', get_applications, name='get_applications'),
    path('applications/<int:application_id>/', manage_application, name='manage_application'),
]
