import uuid
from datetime import datetime
from django.test import TestCase
import pytz

from infrastructure.services.calendar_integration_service import (
    GoogleCalendarAPIClient,
    ICalGenerator,
    CalendarWebhookHandler,
    CalendarAnalyticsService,
)


class GoogleCalendarAPIClientTest(TestCase):
    """Tests for GoogleCalendarAPIClient."""
    
    def test_create_event(self):
        """Test creating event via API."""
        client = GoogleCalendarAPIClient()
        event_id = client.create_event('primary', {
            'title': 'Test Event',
            'start': datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            'end': datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
        })
        
        self.assertIsNotNone(event_id)
        self.assertIn('google-event-', event_id)
        
    def test_update_event(self):
        """Test updating event via API."""
        client = GoogleCalendarAPIClient()
        result = client.update_event('primary', 'event-123', {'title': 'Updated'})
        
        self.assertTrue(result)
        
    def test_delete_event(self):
        """Test deleting event via API."""
        client = GoogleCalendarAPIClient()
        result = client.delete_event('primary', 'event-123')
        
        self.assertTrue(result)


class ICalGeneratorTest(TestCase):
    """Tests for ICalGenerator."""
    
    def test_generate(self):
        """Test generating iCal file."""
        generator = ICalGenerator()
        ical = generator.generate({
            'uid': str(uuid.uuid4()),
            'title': 'Test Event',
            'description': 'Test Description',
            'start': datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            'end': datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            'location': 'Test Location',
        })
        
        self.assertIn('BEGIN:VCALENDAR', ical)
        self.assertIn('Test Event', ical)
        self.assertIn('Test Location', ical)
        self.assertIn('END:VCALENDAR', ical)


class CalendarWebhookHandlerTest(TestCase):
    """Tests for CalendarWebhookHandler."""
    
    def test_handle_google_webhook(self):
        """Test handling Google webhook."""
        handler = CalendarWebhookHandler()
        result = handler.handle_google_webhook({
            'event_id': 'event-123',
            'action': 'updated',
        })
        
        self.assertEqual(result['status'], 'processed')
        self.assertEqual(result['event_id'], 'event-123')
        
    def test_verify_webhook_signature(self):
        """Test verifying webhook signature."""
        handler = CalendarWebhookHandler()
        result = handler.verify_webhook_signature('payload', 'signature')
        
        self.assertTrue(result)


class CalendarAnalyticsServiceTest(TestCase):
    """Tests for CalendarAnalyticsService."""
    
    def test_get_sync_stats(self):
        """Test getting sync statistics."""
        service = CalendarAnalyticsService()
        stats = service.get_sync_stats(uuid.uuid4())
        
        self.assertIn('total_syncs', stats)
        self.assertIn('successful_syncs', stats)
