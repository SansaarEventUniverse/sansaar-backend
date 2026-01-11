import pytest
from domain.models import SharedContent, ContentCollaboration
from infrastructure.repositories.content_repository import ContentRepository

@pytest.mark.django_db
class TestContentRepository:
    def test_get_trending_content(self):
        c1 = SharedContent.objects.create(title='Popular', description='Test', content_type='article', creator_user_id=1, status='published')
        c2 = SharedContent.objects.create(title='Less Popular', description='Test', content_type='document', creator_user_id=1, status='published')
        ContentCollaboration.objects.create(content=c1, user_id=2)
        ContentCollaboration.objects.create(content=c1, user_id=3)
        ContentCollaboration.objects.create(content=c2, user_id=4)
        
        repo = ContentRepository()
        trending = repo.get_trending_content(limit=5)
        assert trending[0].title == 'Popular'
    
    def test_get_content_stats(self):
        content = SharedContent.objects.create(title='Test', description='Test', content_type='link', creator_user_id=1, status='published', is_collaborative=True)
        ContentCollaboration.objects.create(content=content, user_id=2, role='editor')
        ContentCollaboration.objects.create(content=content, user_id=3, role='viewer')
        
        repo = ContentRepository()
        stats = repo.get_content_stats(content.id)
        assert stats['collaborators'] == 2
        assert stats['editors'] == 1
        assert stats['is_collaborative'] is True
