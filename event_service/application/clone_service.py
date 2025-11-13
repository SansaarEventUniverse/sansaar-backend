import uuid
from typing import Dict, List
from django.core.exceptions import ValidationError

from domain.event import Event
from domain.clone import EventClone


class CloneEventService:
    """Service for cloning events."""
    
    def clone_event(self, event_id: uuid.UUID, cloned_by: uuid.UUID,
                   customizations: Dict = None, reason: str = '') -> Event:
        """Clone an event."""
        try:
            original = Event.objects.get(id=event_id, deleted_at__isnull=True)
        except Event.DoesNotExist:
            raise ValidationError("Event not found")
        
        cloned = original.clone_event(cloned_by, customizations)
        
        # Track the clone
        modified_fields = list(customizations.keys()) if customizations else []
        EventClone.objects.create(
            original_event_id=original.id,
            cloned_event_id=cloned.id,
            cloned_by=cloned_by,
            clone_reason=reason,
            fields_modified=modified_fields,
        )
        
        return cloned
    
    def get_clones(self, event_id: uuid.UUID) -> List[Event]:
        """Get all clones of an event."""
        clone_records = EventClone.objects.filter(original_event_id=event_id)
        cloned_ids = [record.cloned_event_id for record in clone_records]
        return list(Event.objects.filter(id__in=cloned_ids, deleted_at__isnull=True))


class BulkCloneService:
    """Service for bulk cloning operations."""
    
    def __init__(self):
        self.clone_service = CloneEventService()
    
    def bulk_clone(self, event_ids: List[uuid.UUID], cloned_by: uuid.UUID,
                  customizations: Dict = None) -> List[Event]:
        """Clone multiple events."""
        cloned_events = []
        
        for event_id in event_ids:
            try:
                cloned = self.clone_service.clone_event(
                    event_id, cloned_by, customizations
                )
                cloned_events.append(cloned)
            except ValidationError:
                continue
        
        return cloned_events
    
    def clone_series(self, event_id: uuid.UUID, cloned_by: uuid.UUID,
                    count: int, interval_days: int = 7) -> List[Event]:
        """Clone event multiple times with date intervals."""
        from datetime import timedelta
        
        if count < 1 or count > 50:
            raise ValidationError("Count must be between 1 and 50")
        
        try:
            original = Event.objects.get(id=event_id, deleted_at__isnull=True)
        except Event.DoesNotExist:
            raise ValidationError("Event not found")
        
        cloned_events = []
        
        for i in range(count):
            offset = timedelta(days=interval_days * (i + 1))
            customizations = {
                'title': f"{original.title} #{i + 1}",
                'start_datetime': original.start_datetime + offset,
                'end_datetime': original.end_datetime + offset,
            }
            
            cloned = self.clone_service.clone_event(
                event_id, cloned_by, customizations, f"Series clone {i + 1}"
            )
            cloned_events.append(cloned)
        
        return cloned_events


class CloneCustomizationService:
    """Service for customizing cloned events."""
    
    def apply_customizations(self, cloned_event_id: uuid.UUID,
                           customizations: Dict) -> Event:
        """Apply customizations to cloned event."""
        try:
            event = Event.objects.get(id=cloned_event_id, deleted_at__isnull=True)
        except Event.DoesNotExist:
            raise ValidationError("Event not found")
        
        for key, value in customizations.items():
            if hasattr(event, key):
                setattr(event, key, value)
        
        event.save()
        return event
    
    def get_clone_info(self, cloned_event_id: uuid.UUID) -> Dict:
        """Get information about a cloned event."""
        try:
            clone_record = EventClone.objects.get(cloned_event_id=cloned_event_id)
            return {
                'original_event_id': str(clone_record.original_event_id),
                'cloned_by': str(clone_record.cloned_by),
                'clone_reason': clone_record.clone_reason,
                'fields_modified': clone_record.fields_modified,
                'created_at': clone_record.created_at,
            }
        except EventClone.DoesNotExist:
            raise ValidationError("Clone record not found")
