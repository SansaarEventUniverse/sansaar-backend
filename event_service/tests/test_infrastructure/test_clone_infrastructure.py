import uuid
from datetime import datetime
from django.test import TestCase
import pytz

from domain.event import Event
from domain.clone import EventClone
from infrastructure.services.clone_infrastructure_service import (
    CloneAnalyticsService,
    CloneRelationshipService,
    CloneOptimizationService,
)


class CloneAnalyticsServiceTest(TestCase):
    """Tests for CloneAnalyticsService."""
    
    def test_get_clone_stats(self):
        """Test getting clone statistics."""
        original = Event.objects.create(
            title='Original Event',
            description='Test',
            start_datetime=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=uuid.uuid4(),
        )
        
        # Create some clones
        for i in range(3):
            cloned = original.clone_event(uuid.uuid4())
            EventClone.objects.create(
                original_event_id=original.id,
                cloned_event_id=cloned.id,
                cloned_by=uuid.uuid4(),
                fields_modified=['title', 'start_datetime'],
            )
        
        service = CloneAnalyticsService()
        stats = service.get_clone_stats(original.id)
        
        self.assertEqual(stats['total_clones'], 3)
        self.assertIn('unique_cloners', stats)
        
    def test_get_popular_clones(self):
        """Test getting popular clones."""
        service = CloneAnalyticsService()
        popular = service.get_popular_clones(5)
        
        self.assertIsInstance(popular, list)


class CloneRelationshipServiceTest(TestCase):
    """Tests for CloneRelationshipService."""
    
    def test_get_clone_tree(self):
        """Test getting clone tree."""
        original = Event.objects.create(
            title='Original Event',
            description='Test',
            start_datetime=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=uuid.uuid4(),
        )
        
        cloned = original.clone_event(uuid.uuid4())
        EventClone.objects.create(
            original_event_id=original.id,
            cloned_event_id=cloned.id,
            cloned_by=uuid.uuid4(),
        )
        
        service = CloneRelationshipService()
        tree = service.get_clone_tree(original.id)
        
        self.assertEqual(tree['original_event_id'], str(original.id))
        self.assertEqual(len(tree['clones']), 1)
        
    def test_find_original(self):
        """Test finding original event."""
        original = Event.objects.create(
            title='Original Event',
            description='Test',
            start_datetime=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=uuid.uuid4(),
        )
        
        cloned = original.clone_event(uuid.uuid4())
        EventClone.objects.create(
            original_event_id=original.id,
            cloned_event_id=cloned.id,
            cloned_by=uuid.uuid4(),
        )
        
        service = CloneRelationshipService()
        found_original = service.find_original(cloned.id)
        
        self.assertEqual(found_original, original.id)


class CloneOptimizationServiceTest(TestCase):
    """Tests for CloneOptimizationService."""
    
    def test_optimize_bulk_clone(self):
        """Test optimizing bulk clone."""
        service = CloneOptimizationService()
        optimization = service.optimize_bulk_clone([uuid.uuid4() for _ in range(5)])
        
        self.assertIn('batch_size', optimization)
        self.assertIn('estimated_time', optimization)
        
    def test_validate_clone_feasibility(self):
        """Test validating clone feasibility."""
        event = Event.objects.create(
            title='Test Event',
            description='Test',
            start_datetime=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=uuid.uuid4(),
        )
        
        service = CloneOptimizationService()
        
        self.assertTrue(service.validate_clone_feasibility(event.id, 10))
        self.assertFalse(service.validate_clone_feasibility(event.id, 200))
