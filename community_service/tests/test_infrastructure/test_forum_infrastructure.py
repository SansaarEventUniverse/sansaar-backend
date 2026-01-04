import pytest
from domain.models import Forum, ForumPost
from infrastructure.repositories.forum_repository import ForumRepository

@pytest.mark.django_db
class TestForumRepository:
    def test_get_by_category(self):
        Forum.objects.create(title="Tech", description="Test", category="technology")
        Forum.objects.create(title="General", description="Test", category="general")
        repo = ForumRepository()
        tech_forums = repo.get_by_category('technology')
        assert tech_forums.count() == 1
    
    def test_search_forums(self):
        Forum.objects.create(title="Python Discussion", description="Talk about Python", category="technology")
        Forum.objects.create(title="Java Forum", description="Java discussions", category="technology")
        repo = ForumRepository()
        results = repo.search('Python')
        assert results.count() == 1
