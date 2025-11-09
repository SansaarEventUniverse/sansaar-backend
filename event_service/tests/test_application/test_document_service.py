import uuid
from django.test import TestCase
from django.core.exceptions import ValidationError

from domain.document import Document
from application.document_service import (
    DocumentUploadService,
    DocumentAccessService,
    DocumentVersioningService,
    DocumentManagementService,
)


class DocumentUploadServiceTest(TestCase):
    """Tests for DocumentUploadService."""
    
    def test_validate_upload_success(self):
        """Test successful upload validation."""
        service = DocumentUploadService()
        service.validate_upload('application/pdf', 1024)
        
    def test_validate_upload_invalid_mime(self):
        """Test upload validation with invalid mime type."""
        service = DocumentUploadService()
        with self.assertRaises(ValidationError):
            service.validate_upload('image/jpeg', 1024)
            
    def test_validate_upload_too_large(self):
        """Test upload validation with file too large."""
        service = DocumentUploadService()
        with self.assertRaises(ValidationError):
            service.validate_upload('application/pdf', 200 * 1024 * 1024)


class DocumentAccessServiceTest(TestCase):
    """Tests for DocumentAccessService."""
    
    def test_check_access(self):
        """Test access checking."""
        doc = Document.objects.create(
            event_id=uuid.uuid4(),
            title='Test Doc',
            document_type='agenda',
            file_name='test.pdf',
            file_size=1024,
            mime_type='application/pdf',
            s3_key='events/docs/test.pdf',
            access_level='registered',
            created_by=uuid.uuid4(),
        )
        
        service = DocumentAccessService()
        self.assertFalse(service.check_access(doc, uuid.uuid4(), 'guest'))
        self.assertTrue(service.check_access(doc, uuid.uuid4(), 'registered'))
        
    def test_get_accessible_documents(self):
        """Test getting accessible documents."""
        event_id = uuid.uuid4()
        Document.objects.create(
            event_id=event_id,
            title='Public Doc',
            document_type='agenda',
            file_name='public.pdf',
            file_size=1024,
            mime_type='application/pdf',
            s3_key='events/docs/public.pdf',
            access_level='public',
            created_by=uuid.uuid4(),
        )
        Document.objects.create(
            event_id=event_id,
            title='Organizer Doc',
            document_type='other',
            file_name='organizer.pdf',
            file_size=1024,
            mime_type='application/pdf',
            s3_key='events/docs/organizer.pdf',
            access_level='organizer',
            created_by=uuid.uuid4(),
        )
        
        service = DocumentAccessService()
        guest_docs = service.get_accessible_documents(event_id, 'guest')
        organizer_docs = service.get_accessible_documents(event_id, 'organizer')
        
        self.assertEqual(len(guest_docs), 1)
        self.assertEqual(len(organizer_docs), 2)


class DocumentVersioningServiceTest(TestCase):
    """Tests for DocumentVersioningService."""
    
    def test_create_version(self):
        """Test creating new version."""
        doc = Document.objects.create(
            event_id=uuid.uuid4(),
            title='Versioned Doc',
            document_type='schedule',
            file_name='schedule.pdf',
            file_size=1024,
            mime_type='application/pdf',
            s3_key='events/docs/schedule_v1.pdf',
            created_by=uuid.uuid4(),
        )
        
        service = DocumentVersioningService()
        new_doc = service.create_version(doc.id, 'events/docs/schedule_v2.pdf', 2048)
        
        self.assertEqual(new_doc.version, 2)
        self.assertEqual(new_doc.previous_version_id, doc.id)
        
    def test_get_version_history(self):
        """Test getting version history."""
        doc_v1 = Document.objects.create(
            event_id=uuid.uuid4(),
            title='Doc',
            document_type='agenda',
            file_name='doc.pdf',
            file_size=1024,
            mime_type='application/pdf',
            s3_key='events/docs/doc_v1.pdf',
            created_by=uuid.uuid4(),
        )
        
        doc_v2 = doc_v1.create_new_version('events/docs/doc_v2.pdf', 2048)
        
        service = DocumentVersioningService()
        history = service.get_version_history(doc_v2.id)
        
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0].version, 2)
        self.assertEqual(history[1].version, 1)


class DocumentManagementServiceTest(TestCase):
    """Tests for DocumentManagementService."""
    
    def test_create_document(self):
        """Test creating document."""
        service = DocumentManagementService()
        doc = service.create_document({
            'event_id': uuid.uuid4(),
            'title': 'New Doc',
            'document_type': 'agenda',
            'file_name': 'new.pdf',
            'file_size': 1024,
            'mime_type': 'application/pdf',
            's3_key': 'events/docs/new.pdf',
            'created_by': uuid.uuid4(),
        })
        
        self.assertIsNotNone(doc.id)
        
    def test_get_document_with_access(self):
        """Test getting document with access."""
        doc = Document.objects.create(
            event_id=uuid.uuid4(),
            title='Test Doc',
            document_type='agenda',
            file_name='test.pdf',
            file_size=1024,
            mime_type='application/pdf',
            s3_key='events/docs/test.pdf',
            access_level='public',
            created_by=uuid.uuid4(),
        )
        
        service = DocumentManagementService()
        retrieved = service.get_document(doc.id, 'guest')
        
        self.assertEqual(retrieved.id, doc.id)
        
    def test_get_document_without_access(self):
        """Test getting document without access."""
        doc = Document.objects.create(
            event_id=uuid.uuid4(),
            title='Private Doc',
            document_type='other',
            file_name='private.pdf',
            file_size=1024,
            mime_type='application/pdf',
            s3_key='events/docs/private.pdf',
            access_level='organizer',
            created_by=uuid.uuid4(),
        )
        
        service = DocumentManagementService()
        with self.assertRaises(ValidationError):
            service.get_document(doc.id, 'guest')
