import uuid
from django.test import TestCase, Client
from django.utils import timezone
from datetime import timedelta

from domain.event import Event


class DateTimeAPITest(TestCase):
    """Tests for DateTime API endpoints."""
    
    def setUp(self):
        self.client = Client()
        self.organizer_id = uuid.uuid4()
        self.venue_id = uuid.uuid4()
        self.now = timezone.now()
        
    def test_export_ical(self):
        """Test iCal export endpoint."""
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
        )
        response = self.client.get(f'/api/events/{event.id}/ical/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/calendar')
        self.assertIn(b'BEGIN:VCALENDAR', response.content)
        
    def test_export_ical_nonexistent(self):
        """Test iCal export for non-existent event."""
        response = self.client.get(f'/api/events/{uuid.uuid4()}/ical/')
        self.assertEqual(response.status_code, 404)
        
    def test_list_timezones(self):
        """Test listing timezones."""
        response = self.client.get('/api/events/timezones/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('timezones', data)
        self.assertGreater(len(data['timezones']), 0)
        
    def test_list_all_timezones(self):
        """Test listing all timezones."""
        response = self.client.get('/api/events/timezones/?common=false')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('timezones', data)
        self.assertGreater(len(data['timezones']), 0)
