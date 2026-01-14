import pytest
from domain.models import Forum, ForumPost
from application.services.forum_service import ForumService
from application.services.post_management_service import PostManagementService
from application.services.moderation_service import ModerationService

@pytest.mark.django_db
class TestForumService:
    def test_create_forum(self):
        service = ForumService()
        data = {
            'title': 'New Forum',
            'description': 'Forum description',
            'category': 'general'
        }
        forum = service.create(data)
        assert forum.title == 'New Forum'
        assert forum.is_active is True
    
    def test_get_active_forums(self):
        Forum.objects.create(title="Active", description="Test", category="general", is_active=True)
        Forum.objects.create(title="Inactive", description="Test", category="general", is_active=False)
        service = ForumService()
        active = service.get_active_forums()
        assert active.count() == 1

@pytest.mark.django_db
class TestPostManagementService:
    def test_create_post(self):
        forum = Forum.objects.create(title="Forum", description="Test", category="general")
        service = PostManagementService()
        data = {
            'forum_id': forum.id,
            'author_name': 'John',
            'author_email': 'john@example.com',
            'title': 'Post Title',
            'content': 'Post content'
        }
        post = service.create(data)
        assert post.title == 'Post Title'
        assert post.status == 'draft'
    
    def test_publish_post(self):
        forum = Forum.objects.create(title="Forum", description="Test", category="general")
        post = ForumPost.objects.create(
            forum=forum,
            author_name="User",
            author_email="user@example.com",
            title="Draft Post",
            content="Content",
            status="draft"
        )
        service = PostManagementService()
        published = service.publish(post.id)
        assert published.status == 'published'
