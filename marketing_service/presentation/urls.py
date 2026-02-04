from django.urls import path
from presentation.views.health_views import health_check
from presentation.views.email_campaign_views import campaigns, send_campaign
from presentation.views.sms_campaign_views import sms_campaign_list_create, send_sms_campaign
from presentation.views.automation_views import workflow_list_create, execute_workflow
from presentation.views.segmentation_views import segment_list_create, analyze_audience
from presentation.views.ab_testing_views import ab_test_list_create, run_ab_test
from presentation.views.social_media_views import social_media_post, schedule_post
from presentation.views.personalization_views import personalize_content, update_preferences, get_personalization
from presentation.views.analytics_views import get_campaign_analytics, generate_report
from presentation.views.intelligence_views import get_intelligence, generate_insights, predictive_analytics
from presentation.views.optimization_views import optimize_campaign, get_optimization, auto_optimize

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
    
    # A/B Testing
    path('ab-tests/', ab_test_list_create, name='ab-test-list-create'),
    path('ab-tests/<int:test_id>/run/', run_ab_test, name='run-ab-test'),
    
    # Social Media
    path('social-media/post/', social_media_post, name='social-media-post'),
    path('social-media/schedule/', schedule_post, name='schedule-post'),
    
    # Personalization
    path('personalization/content/', personalize_content, name='personalize-content'),
    path('users/<int:user_id>/preferences/', update_preferences, name='update-preferences'),
    path('personalization/', get_personalization, name='get-personalization'),
    
    # Campaign Analytics
    path('campaigns/<int:campaign_id>/analytics/', get_campaign_analytics, name='get-campaign-analytics'),
    path('campaigns/<int:campaign_id>/report/', generate_report, name='generate-report'),
    
    # Intelligence
    path('intelligence/', get_intelligence, name='get-intelligence'),
    path('insights/', generate_insights, name='generate-insights'),
    path('predictions/<int:campaign_id>/', predictive_analytics, name='predictive-analytics'),
    
    # Optimization
    path('campaigns/<int:campaign_id>/optimize/', optimize_campaign, name='optimize-campaign'),
    path('campaigns/<int:campaign_id>/optimization/', get_optimization, name='get-optimization'),
    path('campaigns/<int:campaign_id>/auto-optimize/', auto_optimize, name='auto-optimize'),
]
