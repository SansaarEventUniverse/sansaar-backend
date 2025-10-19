from typing import Dict, Any, Optional
import uuid
from django.core.exceptions import ValidationError
from django.utils import timezone

from domain.event import Event, EventDraft


class CreateEventService:
    """Service for creating events with validation."""
    
    def execute(self, data: Dict[str, Any]) -> Event:
        """Create a new event."""
        event = Event(
            title=data['title'],
            description=data['description'],
            organizer_id=data['organizer_id'],
            organization_id=data.get('organization_id'),
            start_datetime=data['start_datetime'],
            end_datetime=data['end_datetime'],
            timezone=data.get('timezone', 'UTC'),
            is_all_day=data.get('is_all_day', False),
            venue_id=data.get('venue_id'),
            is_online=data.get('is_online', False),
            online_url=data.get('online_url'),
            max_attendees=data.get('max_attendees'),
            visibility=data.get('visibility', 'public'),
        )
        event.clean()
        event.save()
        return event


class UpdateEventService:
    """Service for updating events."""
    
    def execute(self, event_id: uuid.UUID, data: Dict[str, Any]) -> Event:
        """Update an existing event."""
        try:
            event = Event.objects.get(id=event_id, deleted_at__isnull=True)
        except Event.DoesNotExist:
            raise ValidationError('Event not found')
        
        # Update fields
        for field, value in data.items():
            if hasattr(event, field):
                setattr(event, field, value)
        
        event.clean()
        event.save()
        return event


class GetEventService:
    """Service for retrieving events."""
    
    def execute(self, event_id: uuid.UUID) -> Event:
        """Get event by ID."""
        try:
            return Event.objects.get(id=event_id, deleted_at__isnull=True)
        except Event.DoesNotExist:
            raise ValidationError('Event not found')


class SaveEventDraftService:
    """Service for auto-saving event drafts."""
    
    def execute(self, organizer_id: uuid.UUID, draft_data: Dict[str, Any], 
                event_id: Optional[uuid.UUID] = None) -> EventDraft:
        """Save or update event draft."""
        # Find existing draft
        if event_id:
            draft = EventDraft.objects.filter(
                event_id=event_id, 
                organizer_id=organizer_id
            ).first()
        else:
            draft = EventDraft.objects.filter(
                organizer_id=organizer_id,
                event_id__isnull=True
            ).order_by('-updated_at').first()
        
        if draft:
            draft.draft_data = draft_data
            draft.save()
        else:
            draft = EventDraft.objects.create(
                event_id=event_id,
                organizer_id=organizer_id,
                draft_data=draft_data,
            )
        
        return draft


class GetEventDraftService:
    """Service for retrieving event drafts."""
    
    def execute(self, organizer_id: uuid.UUID, 
                event_id: Optional[uuid.UUID] = None) -> Optional[EventDraft]:
        """Get latest draft for organizer."""
        if event_id:
            return EventDraft.objects.filter(
                event_id=event_id,
                organizer_id=organizer_id
            ).first()
        
        return EventDraft.objects.filter(
            organizer_id=organizer_id,
            event_id__isnull=True
        ).order_by('-updated_at').first()
