from django.urls import path
from presentation.views.health_views import health_check
from presentation.views.email_campaign_views import campaigns, send_campaign

urlpatterns = [
    # Health Check
    path('health/', health_check, name='health_check'),
    
    # Email Campaigns
    path('email-campaigns/', campaigns, name='campaigns'),
    path('email-campaigns/<int:campaign_id>/send/', send_campaign, name='send_campaign'),
]
