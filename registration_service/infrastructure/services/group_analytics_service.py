from typing import Dict, Any
import uuid
from django.core.cache import cache

from domain.group_registration import GroupRegistration


class GroupAnalyticsService:
    """Service for group registration analytics."""
    
    def get_group_stats(self, event_id: uuid.UUID) -> Dict[str, Any]:
        """Get group statistics for an event."""
        groups = GroupRegistration.objects.filter(event_id=event_id)
        
        total_groups = groups.count()
        confirmed_groups = groups.filter(status='confirmed').count()
        total_members = sum(g.current_size for g in groups)
        
        return {
            'total_groups': total_groups,
            'confirmed_groups': confirmed_groups,
            'total_members': total_members,
            'average_group_size': total_members / total_groups if total_groups > 0 else 0,
        }
    
    def cache_group_stats(self, event_id: uuid.UUID) -> None:
        """Cache group statistics."""
        stats = self.get_group_stats(event_id)
        cache.set(f"group_stats:{event_id}", stats, timeout=300)  # 5 minutes
