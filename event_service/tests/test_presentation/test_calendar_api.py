import uuid
import json
from datetime import datetime
from django.test import TestCase, Client
import pytz

from domain.event import Event
from domain.calendar import CalendarEvent


class CalendarAPITest(TestCase):
    """Tests for Calendar API endpoints."""
    
    def setUp(self):
        self.client = Client()
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            start_datetime=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=uuid.uuid4(),
        )
        
    def test_export_to_calendar(self):
        """Test exporting event to iCal."""
        response = self.client.get(
            f'/api/events/{self.event.id}/calendar/export/'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/calendar')
        self.assertIn('BEGIN:VCALENDAR', response.content.decode())
        
    def test_sync_calendar(self):
        """Test syncing event to calendar."""
        data = {
            'provider': 'google',
            'user_id': str(uuid.uuid4()),
        }
        
        response = self.client.post(
            f'/api/events/{self.event.id}/calendar/sync/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        result = response.json()
        self.assertEqual(result['provider'], 'google')
        self.assertEqual(result['sync_status'], 'synced')
        
    def test_calendar_webhook(self):
        """Test calendar webhook endpoint."""
        data = {
            'event_id': 'external-123',
            'action': 'updated',
            'provider': 'google',
        }
        
        response = self.client.post(
            '/api/events/calendar/webhook/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['status'], 'processed')
        
    def test_get_calendar_syncs(self):
        """Test getting calendar syncs."""
        CalendarEvent.objects.create(
            event_id=self.event.id,
            user_id=uuid.uuid4(),
            provider='google',
            event_title=self.event.title,
            event_start=self.event.start_datetime,
            event_end=self.event.end_datetime,
            event_timezone=self.event.timezone,
        )
        
        response = self.client.get(
            f'/api/events/{self.event.id}/calendar/syncs/'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['provider'], 'google')
