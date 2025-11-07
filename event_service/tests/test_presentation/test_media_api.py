import uuid
import json
from django.test import TestCase, Client
from unittest.mock import patch

from domain.media import MediaGallery, MediaItem


class MediaAPITest(TestCase):
    """Tests for Media API endpoints."""
    
    def setUp(self):
        self.client = Client()
        self.event_id = uuid.uuid4()
        
    @patch('presentation.views.media_views.S3MediaService')
    def test_upload_media(self, mock_s3):
        """Test uploading media via API."""
        mock_s3_instance = mock_s3.return_value
        mock_s3_instance.generate_upload_url.return_value = {
            'upload_url': 'https://s3.amazonaws.com/upload',
            's3_key': 'events/test/photo.jpg',
            'cdn_url': 'https://cdn.example.com/photo.jpg',
        }
        
        data = {
            'file_name': 'photo.jpg',
            'file_type': 'image',
            'file_size': 1024,
            'mime_type': 'image/jpeg',
        }
        
        response = self.client.post(
            f'/api/events/{self.event_id}/media/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('upload_url', response.json())
        self.assertIn('media_id', response.json())
        
    def test_get_media_gallery(self):
        """Test getting media gallery via API."""
        gallery = MediaGallery.objects.create(
            event_id=self.event_id,
            total_items=1,
            total_size_bytes=1024
        )
        MediaItem.objects.create(
            gallery=gallery,
            file_name='photo.jpg',
            file_type='image',
            file_size=1024,
            mime_type='image/jpeg',
            s3_key='events/photo.jpg',
        )
        
        response = self.client.get(
            f'/api/events/{self.event_id}/media/gallery/'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['total_items'], 1)
        self.assertEqual(len(data['items']), 1)
        
    def test_delete_media(self):
        """Test deleting media via API."""
        gallery = MediaGallery.objects.create(event_id=self.event_id)
        item = MediaItem.objects.create(
            gallery=gallery,
            file_name='photo.jpg',
            file_type='image',
            file_size=1024,
            mime_type='image/jpeg',
            s3_key='events/photo.jpg',
        )
        
        response = self.client.delete(
            f'/api/events/{self.event_id}/media/{item.id}/'
        )
        
        self.assertEqual(response.status_code, 204)
        self.assertFalse(MediaItem.objects.filter(id=item.id).exists())
