from typing import Dict, Any
import uuid
from django.core.exceptions import ValidationError

from domain.capacity_rule import CapacityRule
from domain.registration import Registration


class CapacityManagementService:
    """Service for managing event capacity."""
    
    def execute(self, event_id: uuid.UUID) -> Dict[str, Any]:
        """Get capacity information for an event."""
        try:
            rule = CapacityRule.objects.get(event_id=event_id)
        except CapacityRule.DoesNotExist:
            raise ValidationError('Capacity rule not found for event')
        
        confirmed_count = Registration.objects.filter(
            event_id=event_id,
            status='confirmed'
        ).count()
        
        return {
            'event_id': str(event_id),
            'max_capacity': rule.max_capacity,
            'confirmed_count': confirmed_count,
            'available': rule.available_spots(confirmed_count),
            'is_at_capacity': rule.is_at_capacity(confirmed_count),
            'is_near_capacity': rule.is_near_capacity(confirmed_count),
            'warning_threshold': rule.warning_threshold,
        }


class CreateCapacityRuleService:
    """Service for creating capacity rules."""
    
    def execute(self, data: Dict[str, Any]) -> CapacityRule:
        """Create a capacity rule for an event."""
        rule = CapacityRule(
            event_id=data['event_id'],
            max_capacity=data['max_capacity'],
            warning_threshold=data.get('warning_threshold', 80),
            allow_reservations=data.get('allow_reservations', True),
            reservation_timeout_minutes=data.get('reservation_timeout_minutes', 15),
        )
        rule.clean()
        rule.save()
        return rule
