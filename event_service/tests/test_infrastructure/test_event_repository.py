import uuid
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from infrastructure.repositories.event_repository import EventRepository
from domain.event import Event


class EventRepositoryTest(TestCase):
    """Tests for EventRepository."""
    
    def setUp(self):
        self.repository = EventRepository()
        self.organizer_id = uuid.uuid4()
        self.organization_id = uuid.uuid4()
        self.venue_id = uuid.uuid4()
        self.now = timezone.now()
        
    def test_get_organizer_events(self):
        """Test getting organizer events."""
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
        )
        events = self.repository.get_organizer_events(self.organizer_id)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].id, event.id)
        
    def test_get_organizer_events_by_status(self):
        """Test filtering organizer events by status."""
        Event.objects.create(
            title='Draft Event',
            description='Test Description',
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
            status='draft',
        )
        Event.objects.create(
            title='Published Event',
            description='Test Description',
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
            status='published',
        )
        events = self.repository.get_organizer_events(self.organizer_id, status='published')
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].status, 'published')
        
    def test_get_organization_events(self):
        """Test getting organization events."""
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            organizer_id=self.organizer_id,
            organization_id=self.organization_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
        )
        events = self.repository.get_organization_events(self.organization_id)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].id, event.id)
        
    def test_get_public_events(self):
        """Test getting public events."""
        Event.objects.create(
            title='Public Event',
            description='Test Description',
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
            status='published',
            visibility='public',
        )
        Event.objects.create(
            title='Private Event',
            description='Test Description',
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
            status='published',
            visibility='private',
        )
        events = self.repository.get_public_events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].visibility, 'public')
        
    def test_search_events(self):
        """Test searching events."""
        Event.objects.create(
            title='Python Conference',
            description='Test Description',
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
        )
        Event.objects.create(
            title='JavaScript Meetup',
            description='Test Description',
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
        )
        events = self.repository.search_events('Python')
        self.assertEqual(len(events), 1)
        self.assertIn('Python', events[0].title)
        
    def test_excludes_deleted_events(self):
        """Test that deleted events are excluded."""
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
        )
        event.soft_delete()
        events = self.repository.get_organizer_events(self.organizer_id)
        self.assertEqual(len(events), 0)
