import uuid
from django.test import TestCase
from django.core.exceptions import ValidationError

from domain.media import MediaGallery, MediaItem


class MediaGalleryModelTest(TestCase):
    """Tests for MediaGallery model."""
    
    def test_create_gallery(self):
        """Test creating media gallery."""
        gallery = MediaGallery.objects.create(event_id=uuid.uuid4())
        self.assertIsNotNone(gallery.id)
        self.assertEqual(gallery.total_items, 0)
        
    def test_add_item(self):
        """Test adding item to gallery."""
        gallery = MediaGallery.objects.create(event_id=uuid.uuid4())
        gallery.add_item(size_bytes=1024)
        
        gallery.refresh_from_db()
        self.assertEqual(gallery.total_items, 1)
        self.assertEqual(gallery.total_size_bytes, 1024)
        
    def test_remove_item(self):
        """Test removing item from gallery."""
        gallery = MediaGallery.objects.create(
            event_id=uuid.uuid4(),
            total_items=2,
            total_size_bytes=2048
        )
        gallery.remove_item(size_bytes=1024)
        
        gallery.refresh_from_db()
        self.assertEqual(gallery.total_items, 1)
        self.assertEqual(gallery.total_size_bytes, 1024)


class MediaItemModelTest(TestCase):
    """Tests for MediaItem model."""
    
    def setUp(self):
        self.gallery = MediaGallery.objects.create(event_id=uuid.uuid4())
        
    def test_create_media_item(self):
        """Test creating media item."""
        item = MediaItem.objects.create(
            gallery=self.gallery,
            file_name='photo.jpg',
            file_type='image',
            file_size=1024,
            mime_type='image/jpeg',
            s3_key='events/photo.jpg',
        )
        self.assertIsNotNone(item.id)
        
    def test_file_size_validation(self):
        """Test file size validation."""
        item = MediaItem(
            gallery=self.gallery,
            file_name='large.jpg',
            file_type='image',
            file_size=60 * 1024 * 1024,  # 60MB
            mime_type='image/jpeg',
            s3_key='events/large.jpg',
        )
        with self.assertRaises(ValidationError):
            item.clean()
