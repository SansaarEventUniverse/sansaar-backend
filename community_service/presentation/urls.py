from django.urls import path
from presentation.views.health_views import health_check
from presentation.views.forum_views import create_forum, get_forums, create_post
from presentation.views.feedback_views import submit_feedback, get_feedback, feedback_analytics
from presentation.views.connection_views import connect_user, get_connections, update_connection_status, get_recommendations
from presentation.views.interest_group_views import create_group, get_groups, join_group, get_recommendations as get_group_recommendations
from presentation.views.mentorship_views import create_program, get_programs, join_program, get_mentorships

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
]
