import uuid
from datetime import datetime
from django.test import TestCase
from django.core.exceptions import ValidationError
import pytz

from domain.event import Event
from domain.clone import EventClone


class EventCloneTest(TestCase):
    """Tests for EventClone model."""
    
    def test_create_event_clone(self):
        """Test creating event clone record."""
        clone_record = EventClone.objects.create(
            original_event_id=uuid.uuid4(),
            cloned_event_id=uuid.uuid4(),
            cloned_by=uuid.uuid4(),
            clone_reason='Recurring event',
        )
        
        self.assertIsNotNone(clone_record.id)
        self.assertEqual(clone_record.clone_reason, 'Recurring event')


class EventCloningTest(TestCase):
    """Tests for Event cloning methods."""
    
    def test_can_clone(self):
        """Test checking if event can be cloned."""
        event = Event.objects.create(
            title='Test Event',
            description='Test',
            start_datetime=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=uuid.uuid4(),
        )
        
        self.assertTrue(event.can_clone())
        
        event.deleted_at = datetime.now(pytz.UTC)
        event.save()
        
        self.assertFalse(event.can_clone())
        
    def test_clone_event_basic(self):
        """Test basic event cloning."""
        original = Event.objects.create(
            title='Original Event',
            description='Original description',
            start_datetime=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=uuid.uuid4(),
        )
        
        cloned = original.clone_event(uuid.uuid4())
        
        self.assertEqual(cloned.title, 'Original Event (Copy)')
        self.assertEqual(cloned.description, original.description)
        self.assertEqual(cloned.status, 'draft')
        self.assertNotEqual(cloned.id, original.id)
        
    def test_clone_event_with_customizations(self):
        """Test cloning event with customizations."""
        original = Event.objects.create(
            title='Original Event',
            description='Original description',
            start_datetime=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=uuid.uuid4(),
        )
        
        customizations = {
            'title': 'Customized Event',
            'start_datetime': datetime(2026, 3, 1, 10, 0, tzinfo=pytz.UTC),
            'end_datetime': datetime(2026, 3, 1, 12, 0, tzinfo=pytz.UTC),
        }
        
        cloned = original.clone_event(uuid.uuid4(), customizations)
        
        self.assertEqual(cloned.title, 'Customized Event')
        self.assertEqual(cloned.start_datetime, customizations['start_datetime'])
        self.assertEqual(cloned.description, original.description)
        
    def test_clone_deleted_event_fails(self):
        """Test that cloning deleted event fails."""
        event = Event.objects.create(
            title='Deleted Event',
            description='Test',
            start_datetime=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=uuid.uuid4(),
            deleted_at=datetime.now(pytz.UTC),
        )
        
        with self.assertRaises(ValidationError):
            event.clone_event(uuid.uuid4())
