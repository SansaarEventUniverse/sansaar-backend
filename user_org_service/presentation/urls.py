from django.urls import path

from .views.health_views import health_check
from .views.profile_views import get_profile, list_profiles, update_profile, upload_profile_picture

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('profiles/', list_profiles, name='list_profiles'),
    path('profile/<str:user_id>/', get_profile, name='get_profile'),
    path('profile/<str:user_id>/update/', update_profile, name='update_profile'),
    path('profile/<str:user_id>/picture/', upload_profile_picture, name='upload_profile_picture'),
]
