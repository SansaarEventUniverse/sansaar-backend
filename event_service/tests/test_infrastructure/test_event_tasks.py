import uuid
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from infrastructure.tasks.event_tasks import cleanup_old_drafts, auto_complete_events
from domain.event import EventDraft, Event


class EventTasksTest(TestCase):
    """Tests for event Celery tasks."""
    
    def test_cleanup_old_drafts(self):
        """Test cleaning up old drafts."""
        organizer_id = uuid.uuid4()
        
        # Create old draft
        old_draft = EventDraft.objects.create(
            organizer_id=organizer_id,
            draft_data={'title': 'Old Draft'},
        )
        EventDraft.objects.filter(id=old_draft.id).update(
            updated_at=timezone.now() - timedelta(days=31)
        )
        
        # Create recent draft
        recent_draft = EventDraft.objects.create(
            organizer_id=organizer_id,
            draft_data={'title': 'Recent Draft'},
        )
        
        result = cleanup_old_drafts()
        
        self.assertIn('Deleted 1', result)
        self.assertFalse(EventDraft.objects.filter(id=old_draft.id).exists())
        self.assertTrue(EventDraft.objects.filter(id=recent_draft.id).exists())
    
    def test_auto_complete_events(self):
        """Test auto-completing events."""
        organizer_id = uuid.uuid4()
        venue_id = uuid.uuid4()
        now = timezone.now()
        
        # Create event that should be completed
        old_event = Event.objects.create(
            title='Old Event',
            description='Test',
            organizer_id=organizer_id,
            start_datetime=now - timedelta(days=3),
            end_datetime=now - timedelta(days=2),
            venue_id=venue_id,
            status='published',
        )
        
        # Create recent event
        recent_event = Event.objects.create(
            title='Recent Event',
            description='Test',
            organizer_id=organizer_id,
            start_datetime=now - timedelta(hours=2),
            end_datetime=now - timedelta(hours=1),
            venue_id=venue_id,
            status='published',
        )
        
        result = auto_complete_events()
        
        self.assertIn('Auto-completed 1', result)
        old_event.refresh_from_db()
        recent_event.refresh_from_db()
        self.assertEqual(old_event.status, 'completed')
        self.assertEqual(recent_event.status, 'published')
