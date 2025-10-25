from typing import List
import uuid

from domain.waitlist import Waitlist


class WaitlistRepository:
    """Repository for complex waitlist queries."""
    
    def get_event_waitlist(self, event_id: uuid.UUID) -> List[Waitlist]:
        """Get all waitlist entries for an event."""
        return list(Waitlist.objects.filter(
            event_id=event_id,
            is_promoted=False
        ).order_by('position'))
    
    def get_waitlist_count(self, event_id: uuid.UUID) -> int:
        """Get count of users on waitlist."""
        return Waitlist.objects.filter(
            event_id=event_id,
            is_promoted=False
        ).count()
