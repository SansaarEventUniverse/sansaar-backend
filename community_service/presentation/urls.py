from django.urls import path
from presentation.views.health_views import health_check
from presentation.views.forum_views import create_forum, get_forums, create_post
from presentation.views.feedback_views import submit_feedback, get_feedback, feedback_analytics
from presentation.views.connection_views import connect_user, get_connections, update_connection_status, get_recommendations
from presentation.views.interest_group_views import create_group, get_groups, join_group, get_recommendations as get_group_recommendations
from presentation.views.mentorship_views import create_program, get_programs, join_program, get_mentorships
from presentation.views.achievement_views import create_achievement, get_achievements, get_user_achievements, get_user_progress
from presentation.views.content_views import share_content, get_shared_content, collaborate, get_collaborators
from presentation.views.moderation_views import moderation_dashboard, report_content, moderation_actions
from presentation.views.resource_views import upload_resource, search_resources, get_resource_library
from presentation.views.analytics_views import get_community_analytics, get_engagement_report, get_insights_dashboard

urlpatterns = [
    # Health Check
    path('health/', health_check, name='health_check'),
    
    # Community Forums
    path('forums/create/', create_forum, name='create_forum'),
    path('forums/', get_forums, name='get_forums'),
    path('forums/<int:forum_id>/posts/', create_post, name='create_post'),
    
    # Feedback (for events, forums, volunteers)
    path('feedback/submit/', submit_feedback, name='submit_feedback'),
    path('feedback/', get_feedback, name='get_feedback'),
    path('feedback/analytics/', feedback_analytics, name='feedback_analytics'),
    
    # Social Networking
    path('connections/connect/', connect_user, name='connect_user'),
    path('connections/', get_connections, name='get_connections'),
    path('connections/<int:connection_id>/status/', update_connection_status, name='update_connection_status'),
    path('connections/recommendations/', get_recommendations, name='get_recommendations'),
    
    # Interest Groups
    path('interest-groups/create/', create_group, name='create_interest_group'),
    path('interest-groups/', get_groups, name='get_interest_groups'),
    path('interest-groups/<int:group_id>/join/', join_group, name='join_interest_group'),
    path('interest-groups/recommendations/', get_group_recommendations, name='get_group_recommendations'),
    
    # Mentorship Programs
    path('mentorship-programs/create/', create_program, name='create_mentorship_program'),
    path('mentorship-programs/', get_programs, name='get_mentorship_programs'),
    path('mentorship-programs/<int:program_id>/join/', join_program, name='join_mentorship_program'),
    path('mentorships/', get_mentorships, name='get_mentorships'),
    
    # Achievements
    path('achievements/create/', create_achievement, name='create_achievement'),
    path('achievements/', get_achievements, name='get_achievements'),
    path('users/<int:user_id>/achievements/', get_user_achievements, name='get_user_achievements'),
    path('users/<int:user_id>/progress/', get_user_progress, name='get_user_progress'),
    
    # Content Sharing
    path('content/share/', share_content, name='share_content'),
    path('content/shared/', get_shared_content, name='get_shared_content'),
    path('content/<int:content_id>/collaborate/', collaborate, name='collaborate'),
    path('content/<int:content_id>/collaborators/', get_collaborators, name='get_collaborators'),
    
    # Community Moderation
    path('admin/moderation/', moderation_dashboard, name='moderation_dashboard'),
    path('content/<int:content_id>/report/', report_content, name='report_content'),
    path('moderation/actions/', moderation_actions, name='moderation_actions'),
    
    # Resource Sharing
    path('resources/upload/', upload_resource, name='upload_resource'),
    path('resources/search/', search_resources, name='search_resources'),
    path('resource-library/', get_resource_library, name='get_resource_library'),
    
    # Community Analytics
    path('analytics/', get_community_analytics, name='get_community_analytics'),
    path('engagement/', get_engagement_report, name='get_engagement_report'),
    path('insights/', get_insights_dashboard, name='get_insights_dashboard'),
]
