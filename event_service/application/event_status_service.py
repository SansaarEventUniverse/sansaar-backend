import uuid
from django.core.exceptions import ValidationError

from domain.event import Event


class PublishEventService:
    """Service for publishing events."""
    
    def execute(self, event_id: uuid.UUID) -> Event:
        """Publish an event."""
        try:
            event = Event.objects.get(id=event_id, deleted_at__isnull=True)
        except Event.DoesNotExist:
            raise ValidationError('Event not found')
        
        event.publish()
        return event


class UnpublishEventService:
    """Service for unpublishing events."""
    
    def execute(self, event_id: uuid.UUID) -> Event:
        """Unpublish an event."""
        try:
            event = Event.objects.get(id=event_id, deleted_at__isnull=True)
        except Event.DoesNotExist:
            raise ValidationError('Event not found')
        
        event.unpublish()
        return event


class CancelEventService:
    """Service for cancelling events."""
    
    def execute(self, event_id: uuid.UUID) -> Event:
        """Cancel an event."""
        try:
            event = Event.objects.get(id=event_id, deleted_at__isnull=True)
        except Event.DoesNotExist:
            raise ValidationError('Event not found')
        
        event.cancel()
        return event


class CompleteEventService:
    """Service for completing events."""
    
    def execute(self, event_id: uuid.UUID) -> Event:
        """Complete an event."""
        try:
            event = Event.objects.get(id=event_id, deleted_at__isnull=True)
        except Event.DoesNotExist:
            raise ValidationError('Event not found')
        
        event.complete()
        return event
