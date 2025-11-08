import uuid
from django.test import TestCase
from django.core.exceptions import ValidationError

from domain.document import Document


class DocumentTest(TestCase):
    """Tests for Document model."""
    
    def test_create_document(self):
        """Test creating a document."""
        doc = Document.objects.create(
            event_id=uuid.uuid4(),
            title='Event Agenda',
            document_type='agenda',
            file_name='agenda.pdf',
            file_size=1024,
            mime_type='application/pdf',
            s3_key='events/docs/agenda.pdf',
            created_by=uuid.uuid4(),
        )
        
        self.assertEqual(doc.version, 1)
        self.assertEqual(doc.access_level, 'public')
        self.assertFalse(doc.is_required)
        
    def test_validate_file_size(self):
        """Test file size validation."""
        doc = Document(
            event_id=uuid.uuid4(),
            title='Large File',
            document_type='other',
            file_name='large.pdf',
            file_size=200 * 1024 * 1024,
            mime_type='application/pdf',
            s3_key='events/docs/large.pdf',
            created_by=uuid.uuid4(),
        )
        
        with self.assertRaises(ValidationError):
            doc.validate_file_size()
            
    def test_access_control_public(self):
        """Test public access control."""
        doc = Document.objects.create(
            event_id=uuid.uuid4(),
            title='Public Doc',
            document_type='agenda',
            file_name='public.pdf',
            file_size=1024,
            mime_type='application/pdf',
            s3_key='events/docs/public.pdf',
            access_level='public',
            created_by=uuid.uuid4(),
        )
        
        self.assertTrue(doc.can_access('guest'))
        self.assertTrue(doc.can_access('registered'))
        self.assertTrue(doc.can_access('organizer'))
        
    def test_access_control_registered(self):
        """Test registered-only access control."""
        doc = Document.objects.create(
            event_id=uuid.uuid4(),
            title='Registered Doc',
            document_type='guidelines',
            file_name='guidelines.pdf',
            file_size=1024,
            mime_type='application/pdf',
            s3_key='events/docs/guidelines.pdf',
            access_level='registered',
            created_by=uuid.uuid4(),
        )
        
        self.assertFalse(doc.can_access('guest'))
        self.assertTrue(doc.can_access('registered'))
        self.assertTrue(doc.can_access('organizer'))
        
    def test_access_control_organizer(self):
        """Test organizer-only access control."""
        doc = Document.objects.create(
            event_id=uuid.uuid4(),
            title='Organizer Doc',
            document_type='other',
            file_name='internal.pdf',
            file_size=1024,
            mime_type='application/pdf',
            s3_key='events/docs/internal.pdf',
            access_level='organizer',
            created_by=uuid.uuid4(),
        )
        
        self.assertFalse(doc.can_access('guest'))
        self.assertFalse(doc.can_access('registered'))
        self.assertTrue(doc.can_access('organizer'))
        
    def test_increment_downloads(self):
        """Test incrementing download count."""
        doc = Document.objects.create(
            event_id=uuid.uuid4(),
            title='Test Doc',
            document_type='agenda',
            file_name='test.pdf',
            file_size=1024,
            mime_type='application/pdf',
            s3_key='events/docs/test.pdf',
            created_by=uuid.uuid4(),
        )
        
        self.assertEqual(doc.download_count, 0)
        doc.increment_downloads()
        self.assertEqual(doc.download_count, 1)
        
    def test_create_new_version(self):
        """Test creating new document version."""
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
        
        new_doc = doc.create_new_version('events/docs/schedule_v2.pdf', 2048)
        
        self.assertEqual(new_doc.version, 2)
        self.assertEqual(new_doc.previous_version_id, doc.id)
        self.assertEqual(new_doc.file_size, 2048)
        self.assertEqual(new_doc.title, doc.title)
