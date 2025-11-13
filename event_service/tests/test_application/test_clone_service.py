import uuid
from datetime import datetime, timedelta
from django.test import TestCase
from django.core.exceptions import ValidationError
import pytz

from domain.event import Event
from domain.clone import EventClone
from application.clone_service import (
    CloneEventService,
    BulkCloneService,
    CloneCustomizationService,
)


class CloneEventServiceTest(TestCase):
    """Tests for CloneEventService."""
    
    def test_clone_event(self):
        """Test cloning event."""
        original = Event.objects.create(
            title='Original Event',
            description='Test',
            start_datetime=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=uuid.uuid4(),
        )
        
        service = CloneEventService()
        cloned = service.clone_event(original.id, uuid.uuid4())
        
        self.assertIsNotNone(cloned.id)
        self.assertNotEqual(cloned.id, original.id)
        
        # Check clone record was created
        clone_record = EventClone.objects.get(cloned_event_id=cloned.id)
        self.assertEqual(clone_record.original_event_id, original.id)
        
    def test_get_clones(self):
        """Test getting clones of an event."""
        original = Event.objects.create(
            title='Original Event',
            description='Test',
            start_datetime=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=uuid.uuid4(),
        )
        
        service = CloneEventService()
        cloned1 = service.clone_event(original.id, uuid.uuid4())
        cloned2 = service.clone_event(original.id, uuid.uuid4())
        
        clones = service.get_clones(original.id)
        
        self.assertEqual(len(clones), 2)


class BulkCloneServiceTest(TestCase):
    """Tests for BulkCloneService."""
    
    def test_bulk_clone(self):
        """Test bulk cloning events."""
        event1 = Event.objects.create(
            title='Event 1',
            description='Test',
            start_datetime=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=uuid.uuid4(),
        )
        event2 = Event.objects.create(
            title='Event 2',
            description='Test',
            start_datetime=datetime(2026, 2, 2, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 2, 2, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=uuid.uuid4(),
        )
        
        service = BulkCloneService()
        cloned = service.bulk_clone([event1.id, event2.id], uuid.uuid4())
        
        self.assertEqual(len(cloned), 2)
        
    def test_clone_series(self):
        """Test cloning event series."""
        original = Event.objects.create(
            title='Weekly Meetup',
            description='Test',
            start_datetime=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=uuid.uuid4(),
        )
        
        service = BulkCloneService()
        series = service.clone_series(original.id, uuid.uuid4(), count=3, interval_days=7)
        
        self.assertEqual(len(series), 3)
        self.assertEqual(series[0].title, 'Weekly Meetup #1')
        
        # Check dates are offset correctly
        expected_start = original.start_datetime + timedelta(days=7)
        self.assertEqual(series[0].start_datetime, expected_start)


class CloneCustomizationServiceTest(TestCase):
    """Tests for CloneCustomizationService."""
    
    def test_apply_customizations(self):
        """Test applying customizations to cloned event."""
        event = Event.objects.create(
            title='Original Title',
            description='Original description',
            start_datetime=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=uuid.uuid4(),
        )
        
        service = CloneCustomizationService()
        updated = service.apply_customizations(event.id, {
            'title': 'Updated Title',
            'description': 'Updated description',
        })
        
        self.assertEqual(updated.title, 'Updated Title')
        self.assertEqual(updated.description, 'Updated description')
        
    def test_get_clone_info(self):
        """Test getting clone information."""
        original = Event.objects.create(
            title='Original Event',
            description='Test',
            start_datetime=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=uuid.uuid4(),
        )
        
        clone_service = CloneEventService()
        cloned = clone_service.clone_event(original.id, uuid.uuid4(), reason='Test clone')
        
        service = CloneCustomizationService()
        info = service.get_clone_info(cloned.id)
        
        self.assertEqual(info['original_event_id'], str(original.id))
        self.assertEqual(info['clone_reason'], 'Test clone')
