import pytest
from rest_framework.test import APIClient
from domain.models import ResourceLibrary, SharedResource

@pytest.mark.django_db
class TestResourceAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_upload_resource(self):
        """Test uploading resource"""
        library = ResourceLibrary.objects.create(
            name="Templates",
            category='template',
            created_by=1
        )
        response = self.client.post('/api/community/resources/upload/', {
            'library': library.id,
            'title': 'Event Checklist',
            'description': 'Comprehensive event checklist',
            'file_url': 'https://example.com/checklist.pdf',
            'file_type': 'pdf',
            'file_size': 2048,
            'tags': ['planning', 'checklist'],
            'uploaded_by': 1
        }, format='json')
        assert response.status_code == 201
        assert response.data['title'] == 'Event Checklist'

    def test_search_resources_by_title(self):
        """Test searching resources by title"""
        library = ResourceLibrary.objects.create(
            name="Templates",
            category='template',
            created_by=1
        )
        SharedResource.objects.create(
            library=library,
            title='Event Planning Guide',
            file_url='https://example.com/guide.pdf',
            file_type='pdf',
            uploaded_by=1
        )
        SharedResource.objects.create(
            library=library,
            title='Marketing Template',
            file_url='https://example.com/marketing.pdf',
            file_type='pdf',
            uploaded_by=1
        )
        
        response = self.client.get('/api/community/resources/search/?q=Event')
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_search_resources_by_tags(self):
        """Test searching resources by tags"""
        library = ResourceLibrary.objects.create(
            name="Templates",
            category='template',
            created_by=1
        )
        SharedResource.objects.create(
            library=library,
            title='Resource 1',
            file_url='https://example.com/1.pdf',
            file_type='pdf',
            tags=['planning', 'event'],
            uploaded_by=1
        )
        SharedResource.objects.create(
            library=library,
            title='Resource 2',
            file_url='https://example.com/2.pdf',
            file_type='pdf',
            tags=['marketing'],
            uploaded_by=1
        )
        
        response = self.client.get('/api/community/resources/search/?tags=planning')
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_get_resource_library(self):
        """Test getting resource library"""
        ResourceLibrary.objects.create(
            name="Templates",
            category='template',
            created_by=1,
            is_public=True
        )
        ResourceLibrary.objects.create(
            name="Guides",
            category='guide',
            created_by=1,
            is_public=True
        )
        ResourceLibrary.objects.create(
            name="Private",
            category='tool',
            created_by=1,
            is_public=False
        )
        
        response = self.client.get('/api/community/resource-library/')
        assert response.status_code == 200
        assert len(response.data) == 2
