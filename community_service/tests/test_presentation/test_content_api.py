import pytest
from rest_framework.test import APIClient
from domain.models import SharedContent, ContentCollaboration

@pytest.mark.django_db
class TestContentAPI:
    def test_share_content(self):
        client = APIClient()
        data = {
            'title': 'My Article',
            'description': 'Great content',
            'content_type': 'article',
            'creator_user_id': 1
        }
        response = client.post('/api/community/content/share/', data, format='json')
        assert response.status_code == 201
        assert response.data['title'] == 'My Article'
    
    def test_get_shared_content(self):
        SharedContent.objects.create(title='C1', description='Test', content_type='article', creator_user_id=1, status='published')
        SharedContent.objects.create(title='C2', description='Test', content_type='document', creator_user_id=1, status='published')
        client = APIClient()
        response = client.get('/api/community/content/shared/')
        assert response.status_code == 200
        assert len(response.data['results']) == 2
    
    def test_collaborate(self):
        content = SharedContent.objects.create(title='Test', description='Test', content_type='link', creator_user_id=1)
        client = APIClient()
        data = {'user_id': 2, 'role': 'editor'}
        response = client.post(f'/api/community/content/{content.id}/collaborate/', data, format='json')
        assert response.status_code == 201
        assert response.data['user_id'] == 2
        assert response.data['role'] == 'editor'
    
    def test_get_collaborators(self):
        content = SharedContent.objects.create(title='Test', description='Test', content_type='media', creator_user_id=1)
        ContentCollaboration.objects.create(content=content, user_id=2)
        ContentCollaboration.objects.create(content=content, user_id=3)
        client = APIClient()
        response = client.get(f'/api/community/content/{content.id}/collaborators/')
        assert response.status_code == 200
        assert len(response.data['results']) == 2
