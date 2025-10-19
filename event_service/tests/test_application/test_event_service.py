import uuid
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from application.event_service import (
    CreateEventService,
    UpdateEventService,
    GetEventService,
    SaveEventDraftService,
    GetEventDraftService,
)
from domain.event import Event, EventDraft


class CreateEventServiceTest(TestCase):
    """Tests for CreateEventService."""
    
    def setUp(self):
        self.service = CreateEventService()
        self.organizer_id = uuid.uuid4()
        self.venue_id = uuid.uuid4()
        self.now = timezone.now()
        
    def test_create_event(self):
        """Test creating a valid event."""
        data = {
            'title': 'Test Event',
            'description': 'Test Description',
            'organizer_id': self.organizer_id,
            'start_datetime': self.now + timedelta(days=1),
            'end_datetime': self.now + timedelta(days=2),
            'venue_id': self.venue_id,
        }
        event = self.service.execute(data)
        self.assertIsNotNone(event.id)
        self.assertEqual(event.title, 'Test Event')
        
    def test_create_event_validation_error(self):
        """Test validation error on invalid data."""
        data = {
            'title': 'Test Event',
            'description': 'Test Description',
            'organizer_id': self.organizer_id,
            'start_datetime': self.now + timedelta(days=2),
            'end_datetime': self.now + timedelta(days=1),
            'venue_id': self.venue_id,
        }
        with self.assertRaises(ValidationError):
            self.service.execute(data)


class UpdateEventServiceTest(TestCase):
    """Tests for UpdateEventService."""
    
    def setUp(self):
        self.service = UpdateEventService()
        self.organizer_id = uuid.uuid4()
        self.venue_id = uuid.uuid4()
        self.now = timezone.now()
        self.event = Event.objects.create(
            title='Original Title',
            description='Original Description',
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
        )
        
    def test_update_event(self):
        """Test updating an event."""
        data = {'title': 'Updated Title'}
        updated = self.service.execute(self.event.id, data)
        self.assertEqual(updated.title, 'Updated Title')
        
    def test_update_nonexistent_event(self):
        """Test updating non-existent event."""
        with self.assertRaises(ValidationError):
            self.service.execute(uuid.uuid4(), {'title': 'Test'})


class GetEventServiceTest(TestCase):
    """Tests for GetEventService."""
    
    def setUp(self):
        self.service = GetEventService()
        self.organizer_id = uuid.uuid4()
        self.venue_id = uuid.uuid4()
        self.now = timezone.now()
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
        )
        
    def test_get_event(self):
        """Test getting an event."""
        event = self.service.execute(self.event.id)
        self.assertEqual(event.id, self.event.id)
        
    def test_get_nonexistent_event(self):
        """Test getting non-existent event."""
        with self.assertRaises(ValidationError):
            self.service.execute(uuid.uuid4())
            
    def test_get_deleted_event(self):
        """Test getting soft-deleted event."""
        self.event.soft_delete()
        with self.assertRaises(ValidationError):
            self.service.execute(self.event.id)


class SaveEventDraftServiceTest(TestCase):
    """Tests for SaveEventDraftService."""
    
    def setUp(self):
        self.service = SaveEventDraftService()
        self.organizer_id = uuid.uuid4()
        
    def test_save_new_draft(self):
        """Test saving a new draft."""
        draft_data = {'title': 'Draft Event'}
        draft = self.service.execute(self.organizer_id, draft_data)
        self.assertIsNotNone(draft.id)
        self.assertEqual(draft.draft_data['title'], 'Draft Event')
        
    def test_update_existing_draft(self):
        """Test updating existing draft."""
        draft_data = {'title': 'Draft Event'}
        draft1 = self.service.execute(self.organizer_id, draft_data)
        
        updated_data = {'title': 'Updated Draft'}
        draft2 = self.service.execute(self.organizer_id, updated_data)
        
        self.assertEqual(draft1.id, draft2.id)
        self.assertEqual(draft2.draft_data['title'], 'Updated Draft')
        
    def test_save_draft_for_event(self):
        """Test saving draft for existing event."""
        event_id = uuid.uuid4()
        draft_data = {'title': 'Event Draft'}
        draft = self.service.execute(self.organizer_id, draft_data, event_id)
        self.assertEqual(draft.event_id, event_id)


class GetEventDraftServiceTest(TestCase):
    """Tests for GetEventDraftService."""
    
    def setUp(self):
        self.service = GetEventDraftService()
        self.organizer_id = uuid.uuid4()
        
    def test_get_draft(self):
        """Test getting a draft."""
        draft = EventDraft.objects.create(
            organizer_id=self.organizer_id,
            draft_data={'title': 'Draft Event'},
        )
        retrieved = self.service.execute(self.organizer_id)
        self.assertEqual(retrieved.id, draft.id)
        
    def test_get_nonexistent_draft(self):
        """Test getting non-existent draft."""
        draft = self.service.execute(uuid.uuid4())
        self.assertIsNone(draft)
        
    def test_get_draft_for_event(self):
        """Test getting draft for specific event."""
        event_id = uuid.uuid4()
        draft = EventDraft.objects.create(
            event_id=event_id,
            organizer_id=self.organizer_id,
            draft_data={'title': 'Event Draft'},
        )
        retrieved = self.service.execute(self.organizer_id, event_id)
        self.assertEqual(retrieved.id, draft.id)
