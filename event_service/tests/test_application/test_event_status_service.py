import uuid
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from application.event_status_service import (
    PublishEventService,
    UnpublishEventService,
    CancelEventService,
    CompleteEventService,
)
from domain.event import Event


class PublishEventServiceTest(TestCase):
    """Tests for PublishEventService."""
    
    def setUp(self):
        self.service = PublishEventService()
        self.organizer_id = uuid.uuid4()
        self.venue_id = uuid.uuid4()
        self.now = timezone.now()
        
    def test_publish_event(self):
        """Test publishing a draft event."""
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
            status='draft',
        )
        result = self.service.execute(event.id)
        self.assertEqual(result.status, 'published')
        
    def test_publish_nonexistent_event(self):
        """Test publishing non-existent event."""
        with self.assertRaises(ValidationError):
            self.service.execute(uuid.uuid4())


class UnpublishEventServiceTest(TestCase):
    """Tests for UnpublishEventService."""
    
    def setUp(self):
        self.service = UnpublishEventService()
        self.organizer_id = uuid.uuid4()
        self.venue_id = uuid.uuid4()
        self.now = timezone.now()
        
    def test_unpublish_event(self):
        """Test unpublishing a published event."""
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
            status='published',
        )
        result = self.service.execute(event.id)
        self.assertEqual(result.status, 'draft')


class CancelEventServiceTest(TestCase):
    """Tests for CancelEventService."""
    
    def setUp(self):
        self.service = CancelEventService()
        self.organizer_id = uuid.uuid4()
        self.venue_id = uuid.uuid4()
        self.now = timezone.now()
        
    def test_cancel_event(self):
        """Test cancelling a published event."""
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            organizer_id=self.organizer_id,
            start_datetime=self.now + timedelta(days=1),
            end_datetime=self.now + timedelta(days=2),
            venue_id=self.venue_id,
            status='published',
        )
        result = self.service.execute(event.id)
        self.assertEqual(result.status, 'cancelled')


class CompleteEventServiceTest(TestCase):
    """Tests for CompleteEventService."""
    
    def setUp(self):
        self.service = CompleteEventService()
        self.organizer_id = uuid.uuid4()
        self.venue_id = uuid.uuid4()
        self.now = timezone.now()
        
    def test_complete_event(self):
        """Test completing a published event."""
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            organizer_id=self.organizer_id,
            start_datetime=self.now - timedelta(days=2),
            end_datetime=self.now - timedelta(days=1),
            venue_id=self.venue_id,
            status='published',
        )
        result = self.service.execute(event.id)
        self.assertEqual(result.status, 'completed')
