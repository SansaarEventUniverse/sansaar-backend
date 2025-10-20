import uuid
from django.test import TestCase, Client
from django.utils import timezone
from datetime import timedelta

from domain.event import Event


class EventStatusAPITest(TestCase):
    """Tests for Event Status API endpoints."""
    
    def setUp(self):
        self.client = Client()
        self.organizer_id = uuid.uuid4()
        self.venue_id = uuid.uuid4()
        self.now = timezone.now()
        
    def test_publish_event(self):
        """Test publishing an event via API."""
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
            status='draft',
        )
        response = self.client.post(f'/api/events/{event.id}/publish/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'published')
        
    def test_unpublish_event(self):
        """Test unpublishing an event via API."""
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
            status='published',
        )
        response = self.client.post(f'/api/events/{event.id}/unpublish/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'draft')
        
    def test_cancel_event(self):
        """Test cancelling an event via API."""
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
            status='published',
        )
        response = self.client.post(f'/api/events/{event.id}/cancel/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'cancelled')
        
    def test_complete_event(self):
        """Test completing an event via API."""
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            organizer_id=self.organizer_id,
            start_datetime=self.now - timedelta(days=2),
            end_datetime=self.now - timedelta(days=1),
            venue_id=self.venue_id,
            status='published',
        )
        response = self.client.post(f'/api/events/{event.id}/complete/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'completed')
        
    def test_publish_invalid_status(self):
        """Test publishing event with invalid status."""
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
            status='published',
        )
        response = self.client.post(f'/api/events/{event.id}/publish/')
        self.assertEqual(response.status_code, 400)
        
    def test_status_change_nonexistent_event(self):
        """Test status change on non-existent event."""
        response = self.client.post(f'/api/events/{uuid.uuid4()}/publish/')
        self.assertEqual(response.status_code, 400)
