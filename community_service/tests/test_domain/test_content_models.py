import pytest
from domain.models import SharedContent, ContentCollaboration

@pytest.mark.django_db
class TestSharedContent:
    def test_create_shared_content(self):
        content = SharedContent.objects.create(
            title='My Article',
            description='Great article',
            content_type='article',
            creator_user_id=1
        )
        assert content.title == 'My Article'
        assert content.status == 'draft'
    
    def test_publish_content(self):
        content = SharedContent.objects.create(
            title='Test',
            description='Test',
            content_type='document',
            creator_user_id=1
        )
        content.publish()
        assert content.is_published() is True
    
    def test_archive_content(self):
        content = SharedContent.objects.create(
            title='Test',
            description='Test',
            content_type='link',
            creator_user_id=1,
            status='published'
        )
        content.archive()
        assert content.status == 'archived'

@pytest.mark.django_db
class TestContentCollaboration:
    def test_create_collaboration(self):
        content = SharedContent.objects.create(
            title='Test',
            description='Test',
            content_type='media',
            creator_user_id=1,
            is_collaborative=True
        )
        collab = ContentCollaboration.objects.create(content=content, user_id=2)
        assert collab.role == 'viewer'
    
    def test_is_editor(self):
        content = SharedContent.objects.create(
            title='Test',
            description='Test',
            content_type='article',
            creator_user_id=1
        )
        collab = ContentCollaboration.objects.create(content=content, user_id=2, role='editor')
        assert collab.is_editor() is True
    
    def test_promote_to_editor(self):
        content = SharedContent.objects.create(
            title='Test',
            description='Test',
            content_type='document',
            creator_user_id=1
        )
        collab = ContentCollaboration.objects.create(content=content, user_id=2)
        collab.promote_to_editor()
        assert collab.role == 'editor'
