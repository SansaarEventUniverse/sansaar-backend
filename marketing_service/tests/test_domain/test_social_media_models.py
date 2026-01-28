import pytest
from domain.models import SocialMediaPost, SocialPlatform

@pytest.mark.django_db
class TestSocialMediaPost:
    def test_create_post(self):
        """Test creating social media post"""
        post = SocialMediaPost.objects.create(
            content="Check out our new event!",
            platform="facebook",
            status="draft"
        )
        assert post.content == "Check out our new event!"
        assert post.platform == "facebook"

    def test_post_status_choices(self):
        """Test post status validation"""
        post = SocialMediaPost.objects.create(
            content="Test post",
            platform="twitter",
            status="scheduled"
        )
        assert post.status in ['draft', 'scheduled', 'published', 'failed']

    def test_publish_post(self):
        """Test publishing post"""
        post = SocialMediaPost.objects.create(
            content="Test",
            platform="instagram",
            status="scheduled"
        )
        post.publish()
        assert post.status == "published"

    def test_mark_failed(self):
        """Test marking post as failed"""
        post = SocialMediaPost.objects.create(
            content="Test",
            platform="facebook",
            status="scheduled"
        )
        post.mark_failed()
        assert post.status == "failed"

@pytest.mark.django_db
class TestSocialPlatform:
    def test_create_platform(self):
        """Test creating social platform"""
        platform = SocialPlatform.objects.create(
            name="Facebook",
            platform_type="facebook",
            is_active=True
        )
        assert platform.name == "Facebook"
        assert platform.is_active is True

    def test_platform_validation(self):
        """Test platform validation"""
        platform = SocialPlatform.objects.create(
            name="Twitter",
            platform_type="twitter",
            is_active=True
        )
        assert platform.is_valid()
