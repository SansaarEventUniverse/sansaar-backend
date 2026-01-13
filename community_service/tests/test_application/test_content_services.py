import pytest
from domain.models import SharedContent, ContentCollaboration
from application.services.content_service import ContentSharingService, CollaborationService, ContentModerationService

@pytest.mark.django_db
class TestContentSharingService:
    def test_create_content(self):
        service = ContentSharingService()
        content = service.create_content({
            'title': 'My Article',
            'description': 'Great content',
            'content_type': 'article',
            'creator_user_id': 1
        })
        assert content.title == 'My Article'
    
    def test_get_published_content(self):
        SharedContent.objects.create(title='P1', description='Test', content_type='article', creator_user_id=1, status='published')
        SharedContent.objects.create(title='D1', description='Test', content_type='document', creator_user_id=1, status='draft')
        service = ContentSharingService()
        content = service.get_published_content()
        assert content.count() == 1
    
    def test_get_user_content(self):
        SharedContent.objects.create(title='C1', description='Test', content_type='link', creator_user_id=1)
        SharedContent.objects.create(title='C2', description='Test', content_type='media', creator_user_id=1)
        SharedContent.objects.create(title='C3', description='Test', content_type='article', creator_user_id=2)
        service = ContentSharingService()
        content = service.get_user_content(1)
        assert content.count() == 2

@pytest.mark.django_db
class TestCollaborationService:
    def test_add_collaborator(self):
        content = SharedContent.objects.create(title='Test', description='Test', content_type='document', creator_user_id=1)
        service = CollaborationService()
        collab = service.add_collaborator(content.id, 2, 'editor')
        assert collab.user_id == 2
        assert collab.role == 'editor'
    
    def test_get_collaborators(self):
        content = SharedContent.objects.create(title='Test', description='Test', content_type='article', creator_user_id=1)
        ContentCollaboration.objects.create(content=content, user_id=2)
        ContentCollaboration.objects.create(content=content, user_id=3)
        service = CollaborationService()
        collabs = service.get_collaborators(content.id)
        assert collabs.count() == 2
    
    def test_get_user_collaborations(self):
        c1 = SharedContent.objects.create(title='C1', description='Test', content_type='link', creator_user_id=1)
        c2 = SharedContent.objects.create(title='C2', description='Test', content_type='media', creator_user_id=1)
        ContentCollaboration.objects.create(content=c1, user_id=2)
        ContentCollaboration.objects.create(content=c2, user_id=2)
        service = CollaborationService()
        collabs = service.get_user_collaborations(2)
        assert collabs.count() == 2

@pytest.mark.django_db
class TestContentModerationService:
    def test_publish_content(self):
        content = SharedContent.objects.create(title='Test', description='Test', content_type='article', creator_user_id=1)
        service = ContentModerationService()
        updated = service.publish_content(content.id)
        assert updated.is_published()
    
    def test_archive_content(self):
        content = SharedContent.objects.create(title='Test', description='Test', content_type='document', creator_user_id=1, status='published')
        service = ContentModerationService()
        updated = service.archive_content(content.id)
        assert updated.status == 'archived'
