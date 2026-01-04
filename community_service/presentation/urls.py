from django.urls import path
from presentation.views.health_views import health_check
from presentation.views.forum_views import create_forum, get_forums, create_post

urlpatterns = [
    # Health Check
    path('health/', health_check, name='health_check'),
    
    # Community Forums
    path('forums/create/', create_forum, name='create_forum'),
    path('forums/', get_forums, name='get_forums'),
    path('forums/<int:forum_id>/posts/', create_post, name='create_post'),
]
