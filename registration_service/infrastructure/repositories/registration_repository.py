from typing import List
import uuid

from domain.registration import Registration


class RegistrationRepository:
    """Repository for complex registration queries."""
    
    def get_event_registrations(self, event_id: uuid.UUID, 
                               status: str = None) -> List[Registration]:
        """Get all registrations for an event."""
        queryset = Registration.objects.filter(event_id=event_id)
        
        if status:
            queryset = queryset.filter(status=status)
        
        return list(queryset.order_by('-registered_at'))
    
    def get_user_registrations(self, user_id: uuid.UUID) -> List[Registration]:
        """Get all registrations for a user."""
        return list(Registration.objects.filter(
            user_id=user_id
        ).order_by('-registered_at'))
    
    def get_confirmed_count(self, event_id: uuid.UUID) -> int:
        """Get count of confirmed registrations."""
        return Registration.objects.filter(
            event_id=event_id,
            status='confirmed'
        ).count()
