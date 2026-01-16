import pytest
from domain.models import ResourceLibrary, SharedResource

@pytest.mark.django_db
class TestResourceLibrary:
    def test_create_library(self):
        """Test creating resource library"""
        library = ResourceLibrary.objects.create(
            name="Event Planning Resources",
            description="Templates and guides for event planning",
            category='template',
            created_by=1
        )
        assert library.name == "Event Planning Resources"
        assert library.category == 'template'
        assert library.is_public is True

    def test_library_categories(self):
        """Test library category choices"""
        library = ResourceLibrary.objects.create(
            name="Tools Library",
            category='tool',
            created_by=1
        )
        assert library.category == 'tool'

@pytest.mark.django_db
class TestSharedResource:
    def test_create_resource(self):
        """Test creating shared resource"""
        library = ResourceLibrary.objects.create(
            name="Templates",
            category='template',
            created_by=1
        )
        resource = SharedResource.objects.create(
            library=library,
            title="Event Checklist Template",
            description="Comprehensive checklist for events",
            file_url="https://example.com/checklist.pdf",
            file_type="pdf",
            file_size=1024,
            uploaded_by=1
        )
        assert resource.title == "Event Checklist Template"
        assert resource.download_count == 0

    def test_increment_download(self):
        """Test incrementing download count"""
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
        resource.increment_download()
        assert resource.download_count == 1
        resource.increment_download()
        assert resource.download_count == 2

    def test_resource_tags(self):
        """Test resource tags"""
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
            tags=['planning', 'checklist', 'event'],
            uploaded_by=1
        )
        assert len(resource.tags) == 3
        assert 'planning' in resource.tags
