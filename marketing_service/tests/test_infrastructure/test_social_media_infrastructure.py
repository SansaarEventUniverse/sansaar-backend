import pytest
from domain.models import SocialMediaPost
from infrastructure.repositories.social_media_repository import SocialMediaRepository

@pytest.mark.django_db
class TestSocialMediaRepository:
    def test_get_analytics(self):
        """Test getting social media analytics"""
        SocialMediaPost.objects.create(content="Post 1", platform="facebook", status="published")
        SocialMediaPost.objects.create(content="Post 2", platform="twitter", status="failed")
        SocialMediaPost.objects.create(content="Post 3", platform="instagram", status="draft")
        
        repo = SocialMediaRepository()
        analytics = repo.get_analytics()
        
        assert analytics['total_posts'] == 3
        assert analytics['published'] == 1
        assert analytics['failed'] == 1
