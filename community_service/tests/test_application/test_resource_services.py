import pytest
from domain.models import ResourceLibrary, SharedResource
from application.services.resource_service import ResourceSharingService, LibraryManagementService, ResourceSearchService

@pytest.mark.django_db
class TestResourceSharingService:
    def test_upload_resource(self):
        """Test uploading resource"""
        library = ResourceLibrary.objects.create(
            name="Templates",
            category='template',
            created_by=1
        )
        service = ResourceSharingService()
        resource = service.upload_resource({
            'library': library,
            'title': "Event Template",
            'file_url': "https://example.com/template.pdf",
            'file_type': "pdf",
            'uploaded_by': 1
        })
        assert resource.title == "Event Template"

    def test_get_resource(self):
        """Test getting resource"""
        library = ResourceLibrary.objects.create(
            name="Templates",
            category='template',
            created_by=1
        )
        resource = SharedResource.objects.create(
            library=library,
            title="Template",
            file_url="https://example.com/file.pdf",
            file_type="pdf",
            uploaded_by=1
        )
        service = ResourceSharingService()
        result = service.get_resource(resource.id)
        assert result.id == resource.id

    def test_download_resource(self):
        """Test downloading resource increments count"""
        library = ResourceLibrary.objects.create(
            name="Templates",
            category='template',
            created_by=1
        )
        resource = SharedResource.objects.create(
            library=library,
            title="Template",
            file_url="https://example.com/file.pdf",
            file_type="pdf",
            uploaded_by=1
        )
        service = ResourceSharingService()
        result = service.download_resource(resource.id)
        assert result.download_count == 1

@pytest.mark.django_db
class TestLibraryManagementService:
    def test_create_library(self):
        """Test creating library"""
        service = LibraryManagementService()
        library = service.create_library({
            'name': "Event Resources",
            'category': 'template',
            'created_by': 1
        })
        assert library.name == "Event Resources"

    def test_get_library(self):
        """Test getting library"""
        library = ResourceLibrary.objects.create(
            name="Templates",
            category='template',
            created_by=1
        )
        service = LibraryManagementService()
        result = service.get_library(library.id)
        assert result.id == library.id

    def test_get_all_libraries(self):
        """Test getting all public libraries"""
        ResourceLibrary.objects.create(name="Lib1", category='template', created_by=1, is_public=True)
        ResourceLibrary.objects.create(name="Lib2", category='guide', created_by=1, is_public=True)
        ResourceLibrary.objects.create(name="Lib3", category='tool', created_by=1, is_public=False)
        
        service = LibraryManagementService()
        libraries = service.get_all_libraries()
        assert libraries.count() == 2

    def test_get_library_resources(self):
        """Test getting library resources"""
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
            uploaded_by=1
        )
        SharedResource.objects.create(
            library=library,
            title="Resource 2",
            file_url="https://example.com/2.pdf",
            file_type="pdf",
            uploaded_by=1
        )
        
        service = LibraryManagementService()
        resources = service.get_library_resources(library.id)
        assert resources.count() == 2

@pytest.mark.django_db
class TestResourceSearchService:
    def test_search_by_title(self):
        """Test searching by title"""
        library = ResourceLibrary.objects.create(
            name="Templates",
            category='template',
            created_by=1
        )
        SharedResource.objects.create(
            library=library,
            title="Event Planning Template",
            file_url="https://example.com/1.pdf",
            file_type="pdf",
            uploaded_by=1
        )
        SharedResource.objects.create(
            library=library,
            title="Marketing Guide",
            file_url="https://example.com/2.pdf",
            file_type="pdf",
            uploaded_by=1
        )
        
        service = ResourceSearchService()
        results = service.search_by_title("Event")
        assert results.count() == 1

    def test_search_by_tags(self):
        """Test searching by tags"""
        library = ResourceLibrary.objects.create(
            name="Templates",
            category='template',
            created_by=1
        )
        SharedResource.objects.create(
            library=library,
            title="Template 1",
            file_url="https://example.com/1.pdf",
            file_type="pdf",
            tags=['planning', 'event'],
            uploaded_by=1
        )
        SharedResource.objects.create(
            library=library,
            title="Template 2",
            file_url="https://example.com/2.pdf",
            file_type="pdf",
            tags=['marketing'],
            uploaded_by=1
        )
        
        service = ResourceSearchService()
        results = service.search_by_tags(['planning'])
        assert results.count() == 1

    def test_search_by_category(self):
        """Test searching by category"""
        lib1 = ResourceLibrary.objects.create(
            name="Templates",
            category='template',
            created_by=1
        )
        lib2 = ResourceLibrary.objects.create(
            name="Guides",
            category='guide',
            created_by=1
        )
        SharedResource.objects.create(
            library=lib1,
            title="Template",
            file_url="https://example.com/1.pdf",
            file_type="pdf",
            uploaded_by=1
        )
        SharedResource.objects.create(
            library=lib2,
            title="Guide",
            file_url="https://example.com/2.pdf",
            file_type="pdf",
            uploaded_by=1
        )
        
        service = ResourceSearchService()
        results = service.search_by_category('template')
        assert results.count() == 1
