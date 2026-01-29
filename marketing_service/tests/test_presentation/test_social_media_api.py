import pytest
from rest_framework.test import APIClient
from domain.models import SocialMediaPost

@pytest.mark.django_db
class TestSocialMediaAPI:
    def test_create_post(self):
        """Test creating social media post via API"""
        client = APIClient()
        response = client.post('/api/marketing/social-media/post/', {
            'content': 'Check out our new event!',
            'platform': 'facebook'
        }, format='json')
        
        assert response.status_code == 201
        assert response.data['content'] == 'Check out our new event!'

    def test_list_posts(self):
        """Test listing social media posts"""
        SocialMediaPost.objects.create(content="Post 1", platform="facebook")
        
        client = APIClient()
        response = client.get('/api/marketing/social-media/post/')
        
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_schedule_post(self):
        """Test scheduling social media post"""
        from django.utils import timezone
        from datetime import timedelta
        
        post = SocialMediaPost.objects.create(
            content="Test",
            platform="facebook",
            status="draft"
        )
        scheduled_time = (timezone.now() + timedelta(hours=1)).isoformat()
        
        client = APIClient()
        response = client.post('/api/marketing/social-media/schedule/', {
            'post_id': post.id,
            'scheduled_at': scheduled_time
        }, format='json')
        
        assert response.status_code == 200
