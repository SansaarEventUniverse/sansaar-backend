import pytest
from rest_framework.test import APIClient
from domain.models import Forum, ForumPost

@pytest.mark.django_db
class TestForumAPI:
    def test_create_forum(self):
        client = APIClient()
        data = {
            'title': 'New Forum',
            'description': 'Forum description',
            'category': 'general'
        }
        response = client.post('/api/community/forums/create/', data, format='json')
        assert response.status_code == 201
        assert response.data['title'] == 'New Forum'
    
    def test_get_forums(self):
        Forum.objects.create(title="Forum 1", description="Test", category="general")
        client = APIClient()
        response = client.get('/api/community/forums/')
        assert response.status_code == 200
        assert len(response.data['results']) == 1
    
    def test_create_post(self):
        forum = Forum.objects.create(title="Forum", description="Test", category="general")
        client = APIClient()
        data = {
            'author_name': 'John Doe',
            'author_email': 'john@example.com',
            'title': 'Post Title',
            'content': 'Post content'
        }
        response = client.post(f'/api/community/forums/{forum.id}/posts/', data, format='json')
        assert response.status_code == 201
        assert response.data['title'] == 'Post Title'
