import uuid
from django.test import TestCase
from unittest.mock import Mock, patch

from infrastructure.services.s3_document_service import (
    S3DocumentService,
    DocumentScanService,
)


class S3DocumentServiceTest(TestCase):
    """Tests for S3DocumentService."""
    
    @patch('infrastructure.services.s3_document_service.boto3')
    def test_generate_upload_url(self, mock_boto3):
        """Test generating presigned upload URL."""
        mock_client = Mock()
        mock_client.generate_presigned_url.return_value = 'https://s3.amazonaws.com/upload'
        mock_boto3.client.return_value = mock_client
        
        service = S3DocumentService()
        result = service.generate_upload_url(
            event_id=uuid.uuid4(),
            file_name='agenda.pdf',
            content_type='application/pdf'
        )
        
        self.assertIn('upload_url', result)
        self.assertIn('s3_key', result)
        self.assertIn('download_url', result)
        
    @patch('infrastructure.services.s3_document_service.boto3')
    def test_generate_download_url(self, mock_boto3):
        """Test generating presigned download URL."""
        mock_client = Mock()
        mock_client.generate_presigned_url.return_value = 'https://s3.amazonaws.com/download'
        mock_boto3.client.return_value = mock_client
        
        service = S3DocumentService()
        url = service.generate_download_url('events/test/doc.pdf')
        
        self.assertIn('s3.amazonaws.com', url)
        
    @patch('infrastructure.services.s3_document_service.boto3')
    def test_delete_file(self, mock_boto3):
        """Test deleting file from S3."""
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client
        
        service = S3DocumentService()
        service.delete_file('events/test/doc.pdf')
        
        mock_client.delete_object.assert_called_once()


class DocumentScanServiceTest(TestCase):
    """Tests for DocumentScanService."""
    
    def test_scan_document(self):
        """Test document scanning."""
        service = DocumentScanService()
        result = service.scan_document('events/test/doc.pdf')
        
        self.assertTrue(result)
