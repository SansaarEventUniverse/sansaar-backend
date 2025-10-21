import uuid
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from domain.event import Event, EventDraft


class EventModelTest(TestCase):
    """Tests for Event domain model."""
    
    def setUp(self):
        self.organizer_id = uuid.uuid4()
        self.organization_id = uuid.uuid4()
        self.venue_id = uuid.uuid4()
        self.now = timezone.now()
        
    def test_create_event(self):
        """Test creating a valid event."""
        event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
        )
        self.assertIsNotNone(event.id)
        self.assertEqual(event.status, 'draft')
        self.assertEqual(event.visibility, 'public')
        
    def test_event_validation_end_before_start(self):
        """Test validation fails when end is before start."""
        event = Event(
            title="Test Event",
            description="Test Description",
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=2),
            end_datetime=self.now + timedelta(days=1),
            venue_id=self.venue_id,
        )
        with self.assertRaises(ValidationError) as cm:
            event.clean()
        self.assertIn('end_datetime', cm.exception.message_dict)
        
    def test_online_event_requires_url(self):
        """Test online event requires URL."""
        event = Event(
            title="Test Event",
            description="Test Description",
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            is_online=True,
        )
        with self.assertRaises(ValidationError) as cm:
            event.clean()
        self.assertIn('online_url', cm.exception.message_dict)
        
    def test_in_person_event_requires_venue(self):
        """Test in-person event requires venue."""
        event = Event(
            title="Test Event",
            description="Test Description",
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            is_online=False,
        )
        with self.assertRaises(ValidationError) as cm:
            event.clean()
        self.assertIn('venue_id', cm.exception.message_dict)
        
    def test_publish_event(self):
        """Test publishing a draft event."""
        event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
        )
        event.publish()
        self.assertEqual(event.status, 'published')
        
    def test_cannot_publish_non_draft(self):
        """Test cannot publish non-draft event."""
        event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
            status='published',
        )
        with self.assertRaises(ValidationError):
            event.publish()
    
    def test_unpublish_event(self):
        """Test unpublishing an event."""
        event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
            status='published',
        )
        event.unpublish()
        self.assertEqual(event.status, 'draft')
    
    def test_cannot_unpublish_non_published(self):
        """Test cannot unpublish non-published event."""
        event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
            status='draft',
        )
        with self.assertRaises(ValidationError):
            event.unpublish()
            
    def test_cancel_event(self):
        """Test cancelling an event."""
        event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
            status='published',
        )
        event.cancel()
        self.assertEqual(event.status, 'cancelled')
        
    def test_complete_event(self):
        """Test completing an event."""
        event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            organizer_id=self.organizer_id,
            start_datetime=self.now - timedelta(days=2),
            end_datetime=self.now - timedelta(days=1),
            venue_id=self.venue_id,
            status='published',
        )
        event.complete()
        self.assertEqual(event.status, 'completed')
        
    def test_is_past(self):
        """Test is_past method."""
        event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            organizer_id=self.organizer_id,
            start_datetime=self.now - timedelta(days=2),
            end_datetime=self.now - timedelta(days=1),
            venue_id=self.venue_id,
        )
        self.assertTrue(event.is_past())
        
    def test_is_upcoming(self):
        """Test is_upcoming method."""
        event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
        )
        self.assertTrue(event.is_upcoming())
        
    def test_is_ongoing(self):
        """Test is_ongoing method."""
        event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            organizer_id=self.organizer_id,
            start_datetime=self.now - timedelta(hours=1),
            end_datetime=self.now + timedelta(hours=1),
            venue_id=self.venue_id,
        )
        self.assertTrue(event.is_ongoing())
        
    def test_soft_delete(self):
        """Test soft delete."""
        event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
        )
        event.soft_delete()
        self.assertIsNotNone(event.deleted_at)
    
    def test_is_multi_day(self):
        """Test multi-day event detection."""
        event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=3),
            venue_id=self.venue_id,
        )
        self.assertTrue(event.is_multi_day())
        
    def test_is_not_multi_day(self):
        """Test single-day event detection."""
        start = self.now.replace(hour=10, minute=0, second=0, microsecond=0)
        end = self.now.replace(hour=18, minute=0, second=0, microsecond=0)
        event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            organizer_id=self.organizer_id,
            start_datetime=start,
            end_datetime=end,
            venue_id=self.venue_id,
        )
        self.assertFalse(event.is_multi_day())
        
    def test_duration_days(self):
        """Test event duration calculation."""
        event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=3),
            venue_id=self.venue_id,
        )
        self.assertEqual(event.duration_days(), 3)
        
    def test_validate_timezone(self):
        """Test timezone validation."""
        event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
            timezone='America/New_York',
        )
        self.assertTrue(event.validate_timezone())
        
    def test_invalid_timezone(self):
        """Test invalid timezone validation."""
        event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
            timezone='Invalid/Timezone',
        )
        with self.assertRaises(ValidationError):
            event.validate_timezone()


class EventDraftModelTest(TestCase):
    """Tests for EventDraft model."""
    
    def setUp(self):
        self.organizer_id = uuid.uuid4()
        
    def test_create_draft(self):
        """Test creating an event draft."""
        draft = EventDraft.objects.create(
            organizer_id=self.organizer_id,
            draft_data={'title': 'Draft Event'},
        )
        self.assertIsNotNone(draft.id)
        self.assertEqual(draft.draft_data['title'], 'Draft Event')
        
    def test_draft_with_event_id(self):
        """Test draft linked to existing event."""
        event_id = uuid.uuid4()
        draft = EventDraft.objects.create(
            event_id=event_id,
            organizer_id=self.organizer_id,
            draft_data={'title': 'Updated Event'},
        )
        self.assertEqual(draft.event_id, event_id)
