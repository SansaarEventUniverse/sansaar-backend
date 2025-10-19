from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from domain.event import EventDraft


@shared_task
def cleanup_old_drafts():
    """Delete drafts older than 30 days."""
    cutoff = timezone.now() - timedelta(days=30)
    deleted_count = EventDraft.objects.filter(updated_at__lt=cutoff).delete()[0]
    return f"Deleted {deleted_count} old drafts"
