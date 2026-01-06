from django.urls import path
from presentation.views.health_views import health_check
from presentation.views.forum_views import create_forum, get_forums, create_post
from presentation.views.feedback_views import submit_feedback, get_feedback, feedback_analytics
from presentation.views.connection_views import connect_user, get_connections, update_connection_status, get_recommendations

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
]
