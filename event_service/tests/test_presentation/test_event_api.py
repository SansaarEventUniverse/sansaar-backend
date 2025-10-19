import uuid
import json
from django.test import TestCase, Client
from django.utils import timezone
from datetime import timedelta

from domain.event import Event, EventDraft


class EventAPITest(TestCase):
    """Tests for Event API endpoints."""
    
    def setUp(self):
        self.client = Client()
        self.organizer_id = uuid.uuid4()
        self.venue_id = uuid.uuid4()
        self.now = timezone.now()
        
    def test_create_event(self):
        """Test creating an event via API."""
        data = {
            'title': 'Test Event',
            'description': 'Test Description',
            'organizer_id': str(self.organizer_id),
            'start_datetime': (self.now + timedelta(days=1)).isoformat(),
            'end_datetime': (self.now + timedelta(days=2)).isoformat(),
            'venue_id': str(self.venue_id),
        }
        response = self.client.post(
            '/api/events/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['title'], 'Test Event')
        
    def test_create_event_validation_error(self):
        """Test validation error on create."""
        data = {
            'title': 'Test Event',
            'description': 'Test Description',
            'organizer_id': str(self.organizer_id),
            'start_datetime': (self.now + timedelta(days=2)).isoformat(),
            'end_datetime': (self.now + timedelta(days=1)).isoformat(),
            'venue_id': str(self.venue_id),
        }
        response = self.client.post(
            '/api/events/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        
    def test_get_event(self):
        """Test getting an event via API."""
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
        )
        response = self.client.get(f'/api/events/{event.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Test Event')
        
    def test_get_nonexistent_event(self):
        """Test getting non-existent event."""
        response = self.client.get(f'/api/events/{uuid.uuid4()}/')
        self.assertEqual(response.status_code, 404)
        
    def test_update_event(self):
        """Test updating an event via API."""
        event = Event.objects.create(
            title='Original Title',
            description='Test Description',
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
        )
        data = {'title': 'Updated Title'}
        response = self.client.patch(
            f'/api/events/{event.id}/update/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Updated Title')
        
    def test_save_draft(self):
        """Test saving event draft via API."""
        data = {
            'organizer_id': str(self.organizer_id),
            'draft_data': {'title': 'Draft Event'},
        }
        response = self.client.post(
            '/api/events/drafts/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['draft_data']['title'], 'Draft Event')
        
    def test_get_draft(self):
        """Test getting event draft via API."""
        draft = EventDraft.objects.create(
            organizer_id=self.organizer_id,
            draft_data={'title': 'Draft Event'},
        )
        response = self.client.get(
            f'/api/events/drafts/get/?organizer_id={self.organizer_id}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], str(draft.id))
        
    def test_get_draft_missing_organizer_id(self):
        """Test getting draft without organizer_id."""
        response = self.client.get('/api/events/drafts/get/')
        self.assertEqual(response.status_code, 400)
