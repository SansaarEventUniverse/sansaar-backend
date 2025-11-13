import uuid
from typing import Dict, List


class CloneAnalyticsService:
    """Service for clone analytics and reporting."""
    
    def get_clone_stats(self, event_id: uuid.UUID) -> Dict:
        """Get clone statistics for an event."""
        from domain.clone import EventClone
        
        clones = EventClone.objects.filter(original_event_id=event_id)
        
        return {
            'total_clones': clones.count(),
            'unique_cloners': clones.values('cloned_by').distinct().count(),
            'most_modified_fields': self._get_most_modified_fields(clones),
        }
    
    def _get_most_modified_fields(self, clones) -> List[str]:
        """Get most frequently modified fields."""
        field_counts = {}
        
        for clone in clones:
            for field in clone.fields_modified:
                field_counts[field] = field_counts.get(field, 0) + 1
        
        sorted_fields = sorted(field_counts.items(), key=lambda x: x[1], reverse=True)
        return [field for field, _ in sorted_fields[:5]]
    
    def get_popular_clones(self, limit: int = 10) -> List[uuid.UUID]:
        """Get most cloned events."""
        from domain.clone import EventClone
        from django.db.models import Count
        
        popular = EventClone.objects.values('original_event_id').annotate(
            clone_count=Count('id')
        ).order_by('-clone_count')[:limit]
        
        return [item['original_event_id'] for item in popular]


class CloneRelationshipService:
    """Service for tracking clone relationships."""
    
    def get_clone_tree(self, event_id: uuid.UUID) -> Dict:
        """Get clone relationship tree."""
        from domain.clone import EventClone
        
        clones = EventClone.objects.filter(original_event_id=event_id)
        
        return {
            'original_event_id': str(event_id),
            'clones': [
                {
                    'cloned_event_id': str(clone.cloned_event_id),
                    'cloned_by': str(clone.cloned_by),
                    'created_at': clone.created_at.isoformat(),
                }
                for clone in clones
            ]
        }
    
    def find_original(self, cloned_event_id: uuid.UUID) -> uuid.UUID:
        """Find original event from clone."""
        from domain.clone import EventClone
        
        try:
            clone = EventClone.objects.get(cloned_event_id=cloned_event_id)
            return clone.original_event_id
        except EventClone.DoesNotExist:
            return None


class CloneOptimizationService:
    """Service for optimizing cloning operations."""
    
    def optimize_bulk_clone(self, event_ids: List[uuid.UUID]) -> Dict:
        """Optimize bulk cloning strategy."""
        # Mock implementation - would analyze events and suggest optimal strategy
        return {
            'batch_size': min(len(event_ids), 10),
            'estimated_time': len(event_ids) * 0.5,
            'recommended_parallel': True,
        }
    
    def validate_clone_feasibility(self, event_id: uuid.UUID, count: int) -> bool:
        """Validate if cloning is feasible."""
        # Check if event exists and count is reasonable
        from domain.event import Event
        
        try:
            Event.objects.get(id=event_id, deleted_at__isnull=True)
            return 1 <= count <= 100
        except Event.DoesNotExist:
            return False
