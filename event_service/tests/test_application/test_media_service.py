import uuid
from django.test import TestCase
from django.core.exceptions import ValidationError

from domain.media import MediaGallery, MediaItem
from application.media_service import MediaManagementService, MediaUploadService


class MediaManagementServiceTest(TestCase):
    """Tests for MediaManagementService."""
    
    def test_get_or_create_gallery(self):
        """Test getting or creating gallery."""
        service = MediaManagementService()
        event_id = uuid.uuid4()
        
        gallery = service.get_or_create_gallery(event_id)
        self.assertIsNotNone(gallery.id)
        
    def test_add_media_item(self):
        """Test adding media item."""
        service = MediaManagementService()
        event_id = uuid.uuid4()
        
        data = {
            'file_name': 'photo.jpg',
            'file_type': 'image',
            'file_size': 1024,
            'mime_type': 'image/jpeg',
            's3_key': 'events/photo.jpg',
        }
        
        item = service.add_media_item(event_id, data)
        self.assertIsNotNone(item.id)
        
        # Verify gallery updated
        gallery = MediaGallery.objects.get(event_id=event_id)
        self.assertEqual(gallery.total_items, 1)


class MediaUploadServiceTest(TestCase):
    """Tests for MediaUploadService."""
    
    def test_validate_upload_success(self):
        """Test successful upload validation."""
        service = MediaUploadService()
        
        result = service.validate_upload(
            file_type='image',
            mime_type='image/jpeg',
            file_size=1024
        )
        self.assertTrue(result)
        
    def test_validate_upload_file_too_large(self):
        """Test validation fails for large file."""
        service = MediaUploadService()
        
        with self.assertRaises(ValidationError):
            service.validate_upload(
                file_type='image',
                mime_type='image/jpeg',
                file_size=60 * 1024 * 1024
            )
            
    def test_validate_upload_invalid_mime_type(self):
        """Test validation fails for invalid mime type."""
        service = MediaUploadService()
        
        with self.assertRaises(ValidationError):
            service.validate_upload(
                file_type='image',
                mime_type='application/exe',
                file_size=1024
            )
