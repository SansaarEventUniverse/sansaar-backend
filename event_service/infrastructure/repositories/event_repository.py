from typing import List, Optional
import uuid
from django.db.models import Q

from domain.event import Event


class EventRepository:
    """Repository for complex event queries."""
    
    def get_organizer_events(self, organizer_id: uuid.UUID, 
                            status: Optional[str] = None) -> List[Event]:
        """Get all events for an organizer."""
        queryset = Event.objects.filter(
            organizer_id=organizer_id,
            deleted_at__isnull=True
        )
        if status:
            queryset = queryset.filter(status=status)
        return list(queryset.order_by('-created_at'))
    
    def get_organization_events(self, organization_id: uuid.UUID,
                               status: Optional[str] = None) -> List[Event]:
        """Get all events for an organization."""
        queryset = Event.objects.filter(
            organization_id=organization_id,
            deleted_at__isnull=True
        )
        if status:
            queryset = queryset.filter(status=status)
        return list(queryset.order_by('-created_at'))
    
    def get_public_events(self, status: str = 'published') -> List[Event]:
        """Get all public events."""
        return list(Event.objects.filter(
            visibility='public',
            status=status,
            deleted_at__isnull=True
        ).order_by('start_datetime'))
    
    def search_events(self, query: str) -> List[Event]:
        """Search events by title or description."""
        return list(Event.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            deleted_at__isnull=True
        ).order_by('-created_at'))
