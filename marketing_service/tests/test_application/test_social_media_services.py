import pytest
from domain.models import SocialMediaPost, SocialPlatform
from application.services.social_media_service import SocialMediaService, PlatformIntegrationService, ContentSchedulingService

@pytest.mark.django_db
class TestSocialMediaService:
    def test_create_post(self):
        """Test creating social media post"""
        service = SocialMediaService()
        post = service.create_post({
            'content': 'Check out our event!',
            'platform': 'facebook'
        })
        assert post.content == 'Check out our event!'

    def test_get_posts(self):
        """Test getting posts"""
        SocialMediaPost.objects.create(content="Post 1", platform="facebook")
        SocialMediaPost.objects.create(content="Post 2", platform="twitter")
        
        service = SocialMediaService()
        posts = service.get_posts()
        assert posts.count() == 2

@pytest.mark.django_db
class TestPlatformIntegrationService:
    def test_connect_platform(self):
        """Test connecting platform"""
        service = PlatformIntegrationService()
        platform = service.connect_platform({
            'name': 'Facebook',
            'platform_type': 'facebook'
        })
        assert platform.name == 'Facebook'

@pytest.mark.django_db
class TestContentSchedulingService:
    def test_schedule_post(self):
        """Test scheduling post"""
        from django.utils import timezone
        from datetime import timedelta
        
        post = SocialMediaPost.objects.create(
            content="Test",
            platform="facebook",
            status="draft"
        )
        scheduled_time = timezone.now() + timedelta(hours=1)
        
        service = ContentSchedulingService()
        service.schedule_post(post.id, scheduled_time)
        
        post.refresh_from_db()
        assert post.status == 'scheduled'
