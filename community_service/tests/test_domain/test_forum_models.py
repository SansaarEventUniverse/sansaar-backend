import pytest
from django.utils import timezone
from domain.models import Forum, ForumPost

@pytest.mark.django_db
class TestForum:
    def test_create_forum(self):
        forum = Forum.objects.create(
            title="General Discussion",
            description="Talk about anything",
            category="general"
        )
        assert forum.title == "General Discussion"
        assert forum.is_active is True
    
    def test_forum_is_active(self):
        forum = Forum.objects.create(
            title="Tech Talk",
            description="Technology discussions",
            category="technology",
            is_active=True
        )
        assert forum.is_active is True
    
    def test_forum_deactivate(self):
        forum = Forum.objects.create(
            title="Old Forum",
            description="Archived forum",
            category="archived"
        )
        forum.deactivate()
        assert forum.is_active is False

@pytest.mark.django_db
class TestForumPost:
    def test_create_post(self):
        forum = Forum.objects.create(
            title="Community",
            description="Community forum",
            category="community"
        )
        post = ForumPost.objects.create(
            forum=forum,
            author_name="John Doe",
            author_email="john@example.com",
            title="Hello World",
            content="This is my first post",
            status="published"
        )
        assert post.title == "Hello World"
        assert post.status == "published"
    
    def test_post_is_published(self):
        forum = Forum.objects.create(
            title="News",
            description="News forum",
            category="news"
        )
        post = ForumPost.objects.create(
            forum=forum,
            author_name="Jane",
            author_email="jane@example.com",
            title="Breaking News",
            content="Important update",
            status="published"
        )
        assert post.is_published() is True
    
    def test_post_moderate(self):
        forum = Forum.objects.create(
            title="Moderated",
            description="Moderated forum",
            category="moderated"
        )
        post = ForumPost.objects.create(
            forum=forum,
            author_name="User",
            author_email="user@example.com",
            title="Test Post",
            content="Test content",
            status="published"
        )
        post.moderate()
        assert post.status == "moderated"
