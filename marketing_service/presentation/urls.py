from django.urls import path
from presentation.views.health_views import health_check
from presentation.views.email_campaign_views import campaigns, send_campaign
from presentation.views.sms_campaign_views import sms_campaign_list_create, send_sms_campaign

urlpatterns = [
    # Health Check
    path('health/', health_check, name='health_check'),
    
    # Email Campaigns
    path('email-campaigns/', campaigns, name='campaigns'),
    path('email-campaigns/<int:campaign_id>/send/', send_campaign, name='send_campaign'),
    
    # SMS Campaigns
    path('sms-campaigns/', sms_campaign_list_create, name='sms-campaign-list-create'),
    path('sms-campaigns/<int:campaign_id>/send/', send_sms_campaign, name='send-sms-campaign'),
]
