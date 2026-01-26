from django.urls import path
from presentation.views.health_views import health_check
from presentation.views.email_campaign_views import campaigns, send_campaign
from presentation.views.sms_campaign_views import sms_campaign_list_create, send_sms_campaign
from presentation.views.automation_views import workflow_list_create, execute_workflow
from presentation.views.segmentation_views import segment_list_create, analyze_audience

urlpatterns = [
    # Health Check
    path('health/', health_check, name='health_check'),
    
    # Email Campaigns
    path('email-campaigns/', campaigns, name='campaigns'),
    path('email-campaigns/<int:campaign_id>/send/', send_campaign, name='send_campaign'),
    
    # SMS Campaigns
    path('sms-campaigns/', sms_campaign_list_create, name='sms-campaign-list-create'),
    path('sms-campaigns/<int:campaign_id>/send/', send_sms_campaign, name='send-sms-campaign'),
    
    # Automation Workflows
    path('automation/workflows/', workflow_list_create, name='workflow-list-create'),
    path('automation/workflows/<int:workflow_id>/execute/', execute_workflow, name='execute-workflow'),
    
    # Audience Segmentation
    path('audience/segments/', segment_list_create, name='segment-list-create'),
    path('audience/analyze/', analyze_audience, name='analyze-audience'),
]
