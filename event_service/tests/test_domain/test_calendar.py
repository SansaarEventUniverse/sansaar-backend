import uuid
from datetime import datetime
from django.test import TestCase
from django.core.exceptions import ValidationError
import pytz

from domain.calendar import CalendarEvent


class CalendarEventTest(TestCase):
    """Tests for CalendarEvent model."""
    
    def test_create_calendar_event(self):
        """Test creating a calendar event."""
        event = CalendarEvent.objects.create(
            event_id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            provider='google',
            event_title='Test Event',
            event_start=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            event_end=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            event_timezone='America/New_York',
        )
        
        self.assertEqual(event.sync_status, 'pending')
        self.assertIsNone(event.last_synced_at)
        
    def test_validate_timezone(self):
        """Test timezone validation."""
        event = CalendarEvent(
            event_id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            provider='google',
            event_title='Test Event',
            event_start=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            event_end=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            event_timezone='Invalid/Timezone',
        )
        
        with self.assertRaises(ValidationError):
            event.validate_timezone()
            
    def test_mark_synced(self):
        """Test marking event as synced."""
        event = CalendarEvent.objects.create(
            event_id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            provider='google',
            event_title='Test Event',
            event_start=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            event_end=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            event_timezone='UTC',
        )
        
        event.mark_synced('external-123')
        
        self.assertEqual(event.sync_status, 'synced')
        self.assertEqual(event.external_event_id, 'external-123')
        self.assertIsNotNone(event.last_synced_at)
        
    def test_mark_failed(self):
        """Test marking event sync as failed."""
        event = CalendarEvent.objects.create(
            event_id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            provider='google',
            event_title='Test Event',
            event_start=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            event_end=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            event_timezone='UTC',
        )
        
        event.mark_failed('API error')
        
        self.assertEqual(event.sync_status, 'failed')
        self.assertEqual(event.sync_error, 'API error')
        
    def test_needs_sync(self):
        """Test checking if event needs sync."""
        event = CalendarEvent.objects.create(
            event_id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            provider='google',
            event_title='Test Event',
            event_start=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            event_end=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            event_timezone='UTC',
        )
        
        self.assertTrue(event.needs_sync())
        
        event.mark_synced('external-123')
        self.assertFalse(event.needs_sync())
        
    def test_convert_to_timezone(self):
        """Test converting event to different timezone."""
        event = CalendarEvent.objects.create(
            event_id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            provider='google',
            event_title='Test Event',
            event_start=datetime(2026, 2, 1, 15, 0, tzinfo=pytz.UTC),
            event_end=datetime(2026, 2, 1, 17, 0, tzinfo=pytz.UTC),
            event_timezone='UTC',
        )
        
        start_ny, end_ny = event.convert_to_timezone('America/New_York')
        
        self.assertEqual(start_ny.hour, 10)
        self.assertEqual(end_ny.hour, 12)
