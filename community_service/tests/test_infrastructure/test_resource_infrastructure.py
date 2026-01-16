import pytest
from domain.models import ResourceLibrary, SharedResource
from infrastructure.repositories.resource_repository import ResourceRepository

@pytest.mark.django_db
class TestResourceRepository:
    def test_get_library_stats(self):
        """Test getting library statistics"""
        library = ResourceLibrary.objects.create(
            name="Templates",
            category='template',
            created_by=1
        )
        SharedResource.objects.create(
            library=library,
            title="Resource 1",
            file_url="https://example.com/1.pdf",
            file_type="pdf",
            download_count=10,
            uploaded_by=1
        )
        SharedResource.objects.create(
            library=library,
            title="Resource 2",
            file_url="https://example.com/2.docx",
            file_type="docx",
            download_count=5,
            uploaded_by=1
        )
        
        repo = ResourceRepository()
        stats = repo.get_library_stats(library.id)
        
        assert stats['total_resources'] == 2
        assert stats['total_downloads'] == 15
        assert len(stats['file_types']) == 2

    def test_get_popular_resources(self):
        """Test getting popular resources"""
        library = ResourceLibrary.objects.create(
            name="Templates",
            category='template',
            created_by=1
        )
        r1 = SharedResource.objects.create(
            library=library,
            title="Popular",
            file_url="https://example.com/1.pdf",
            file_type="pdf",
            download_count=100,
            uploaded_by=1
        )
        SharedResource.objects.create(
            library=library,
            title="Less Popular",
            file_url="https://example.com/2.pdf",
            file_type="pdf",
            download_count=10,
            uploaded_by=1
        )
        
        repo = ResourceRepository()
        popular = repo.get_popular_resources(limit=1)
        assert popular[0].id == r1.id

    def test_get_recent_resources(self):
        """Test getting recent resources"""
        library = ResourceLibrary.objects.create(
            name="Templates",
            category='template',
            created_by=1
        )
        SharedResource.objects.create(
            library=library,
            title="Old",
            file_url="https://example.com/1.pdf",
            file_type="pdf",
            uploaded_by=1
        )
        r2 = SharedResource.objects.create(
            library=library,
            title="Recent",
            file_url="https://example.com/2.pdf",
            file_type="pdf",
            uploaded_by=1
        )
        
        repo = ResourceRepository()
        recent = repo.get_recent_resources(limit=1)
        assert recent[0].id == r2.id
