import uuid
from django.test import TestCase
from unittest.mock import Mock, patch

from infrastructure.services.s3_media_service import S3MediaService


class S3MediaServiceTest(TestCase):
    """Tests for S3MediaService."""
    
    @patch('infrastructure.services.s3_media_service.boto3')
    def test_generate_upload_url(self, mock_boto3):
        """Test generating presigned upload URL."""
        mock_client = Mock()
        mock_client.generate_presigned_url.return_value = 'https://s3.amazonaws.com/upload'
        mock_boto3.client.return_value = mock_client
        
        service = S3MediaService()
        result = service.generate_upload_url(
            event_id=uuid.uuid4(),
            file_name='photo.jpg',
            content_type='image/jpeg'
        )
        
        self.assertIn('upload_url', result)
        self.assertIn('s3_key', result)
        self.assertIn('cdn_url', result)
        
    @patch('infrastructure.services.s3_media_service.boto3')
    def test_delete_file(self, mock_boto3):
        """Test deleting file from S3."""
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client
        
        service = S3MediaService()
        service.delete_file('events/test/photo.jpg')
        
        mock_client.delete_object.assert_called_once()
