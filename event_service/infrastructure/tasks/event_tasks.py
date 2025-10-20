from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from domain.event import EventDraft, Event


@shared_task
def cleanup_old_drafts():
    """Delete drafts older than 30 days."""
    cutoff = timezone.now() - timedelta(days=30)
    deleted_count = EventDraft.objects.filter(updated_at__lt=cutoff).delete()[0]
    return f"Deleted {deleted_count} old drafts"


@shared_task
def auto_complete_events():
    """Auto-complete events 24 hours after end time."""
    cutoff = timezone.now() - timedelta(hours=24)
    events = Event.objects.filter(
        status='published',
        end_datetime__lt=cutoff,
        deleted_at__isnull=True
    )
    
    completed_count = 0
    for event in events:
        try:
            event.complete()
            completed_count += 1
        except Exception:
            pass
    
    return f"Auto-completed {completed_count} events"
