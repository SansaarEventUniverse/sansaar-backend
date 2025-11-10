import uuid
import json
from django.test import TestCase, Client
from unittest.mock import patch

from domain.document import Document


class DocumentAPITest(TestCase):
    """Tests for Document API endpoints."""
    
    def setUp(self):
        self.client = Client()
        self.event_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        
    @patch('presentation.views.document_views.S3DocumentService')
    def test_upload_document(self, mock_s3):
        """Test uploading document via API."""
        mock_s3_instance = mock_s3.return_value
        mock_s3_instance.generate_upload_url.return_value = {
            'upload_url': 'https://s3.amazonaws.com/upload',
            's3_key': 'events/test/agenda.pdf',
            'download_url': 'https://cdn.example.com/agenda.pdf',
        }
        
        data = {
            'title': 'Event Agenda',
            'description': 'Detailed agenda',
            'document_type': 'agenda',
            'file_name': 'agenda.pdf',
            'file_size': 1024,
            'mime_type': 'application/pdf',
            'access_level': 'public',
            'created_by': str(self.user_id),
        }
        
        response = self.client.post(
            f'/api/events/{self.event_id}/documents/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('upload_url', response.json())
        self.assertIn('document_id', response.json())
        
    def test_get_documents(self):
        """Test getting documents via API."""
        Document.objects.create(
            event_id=self.event_id,
            title='Public Doc',
            document_type='agenda',
            file_name='agenda.pdf',
            file_size=1024,
            mime_type='application/pdf',
            s3_key='events/docs/agenda.pdf',
            access_level='public',
            created_by=self.user_id,
        )
        Document.objects.create(
            event_id=self.event_id,
            title='Organizer Doc',
            document_type='other',
            file_name='internal.pdf',
            file_size=1024,
            mime_type='application/pdf',
            s3_key='events/docs/internal.pdf',
            access_level='organizer',
            created_by=self.user_id,
        )
        
        response = self.client.get(
            f'/api/events/{self.event_id}/documents/list/?role=guest'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        
    @patch('presentation.views.document_views.S3DocumentService')
    def test_download_document(self, mock_s3):
        """Test downloading document via API."""
        doc = Document.objects.create(
            event_id=self.event_id,
            title='Test Doc',
            document_type='agenda',
            file_name='test.pdf',
            file_size=1024,
            mime_type='application/pdf',
            s3_key='events/docs/test.pdf',
            access_level='public',
            created_by=self.user_id,
        )
        
        mock_s3_instance = mock_s3.return_value
        mock_s3_instance.generate_download_url.return_value = 'https://s3.amazonaws.com/download'
        
        response = self.client.get(
            f'/api/events/{self.event_id}/documents/{doc.id}/?role=guest'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('download_url', data)
        
        doc.refresh_from_db()
        self.assertEqual(doc.download_count, 1)
        
    @patch('presentation.views.document_views.S3DocumentService')
    def test_delete_document(self, mock_s3):
        """Test deleting document via API."""
        doc = Document.objects.create(
            event_id=self.event_id,
            title='Delete Me',
            document_type='other',
            file_name='delete.pdf',
            file_size=1024,
            mime_type='application/pdf',
            s3_key='events/docs/delete.pdf',
            created_by=self.user_id,
        )
        
        mock_s3_instance = mock_s3.return_value
        
        response = self.client.delete(
            f'/api/events/{self.event_id}/documents/{doc.id}/delete/'
        )
        
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Document.objects.filter(id=doc.id).exists())
        mock_s3_instance.delete_file.assert_called_once()
