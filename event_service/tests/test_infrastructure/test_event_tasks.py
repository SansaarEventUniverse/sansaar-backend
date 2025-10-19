import uuid
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from infrastructure.tasks.event_tasks import cleanup_old_drafts
from domain.event import EventDraft


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
