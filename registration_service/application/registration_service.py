from typing import Dict, Any
import uuid
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from domain.registration import Registration


class RegisterForEventService:
    """Service for registering users for events."""
    
    def execute(self, data: Dict[str, Any]) -> Registration:
        """Register a user for an event."""
        try:
            registration = Registration(
                event_id=data['event_id'],
                user_id=data['user_id'],
                attendee_name=data['attendee_name'],
                attendee_email=data['attendee_email'],
                attendee_phone=data.get('attendee_phone', ''),
                status=data.get('status', 'confirmed'),
            )
            registration.clean()
            registration.save()
            return registration
        except IntegrityError:
            raise ValidationError('User is already registered for this event')


class CancelRegistrationService:
    """Service for cancelling registrations."""
    
    def execute(self, event_id: uuid.UUID, user_id: uuid.UUID) -> Registration:
        """Cancel a registration."""
        try:
            registration = Registration.objects.get(
                event_id=event_id,
                user_id=user_id
            )
        except Registration.DoesNotExist:
            raise ValidationError('Registration not found')
        
        registration.cancel()
        return registration


class CheckCapacityService:
    """Service for checking event capacity."""
    
    def execute(self, event_id: uuid.UUID, max_capacity: int) -> Dict[str, Any]:
        """Check if event has capacity."""
        confirmed_count = Registration.objects.filter(
            event_id=event_id,
            status='confirmed'
        ).count()
        
        available = max_capacity - confirmed_count
        has_capacity = available > 0
        
        return {
            'event_id': str(event_id),
            'max_capacity': max_capacity,
            'confirmed_count': confirmed_count,
            'available': available,
            'has_capacity': has_capacity,
        }


class GetRegistrationService:
    """Service for retrieving registration."""
    
    def execute(self, event_id: uuid.UUID, user_id: uuid.UUID) -> Registration:
        """Get registration by event and user."""
        try:
            return Registration.objects.get(
                event_id=event_id,
                user_id=user_id
            )
        except Registration.DoesNotExist:
            raise ValidationError('Registration not found')
