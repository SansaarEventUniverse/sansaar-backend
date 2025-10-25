from typing import Dict, Any, List
import uuid
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db import models

from domain.waitlist import Waitlist
from domain.registration import Registration


class JoinWaitlistService:
    """Service for joining event waitlist."""
    
    def execute(self, data: Dict[str, Any]) -> Waitlist:
        """Add user to waitlist."""
        try:
            # Get next position
            last_position = Waitlist.objects.filter(
                event_id=data['event_id']
            ).order_by('-position').first()
            
            next_position = (last_position.position + 1) if last_position else 1
            
            waitlist = Waitlist(
                event_id=data['event_id'],
                user_id=data['user_id'],
                position=next_position,
                priority=data.get('priority', 0),
            )
            waitlist.save()
            return waitlist
        except IntegrityError:
            raise ValidationError('User is already on waitlist for this event')


class LeaveWaitlistService:
    """Service for leaving waitlist."""
    
    def execute(self, event_id: uuid.UUID, user_id: uuid.UUID) -> Waitlist:
        """Remove user from waitlist."""
        try:
            waitlist = Waitlist.objects.get(
                event_id=event_id,
                user_id=user_id,
                is_promoted=False
            )
        except Waitlist.DoesNotExist:
            raise ValidationError('Waitlist entry not found')
        
        position = waitlist.position
        waitlist.delete()
        
        # Update positions of remaining waitlist entries
        Waitlist.objects.filter(
            event_id=event_id,
            position__gt=position
        ).update(position=models.F('position') - 1)
        
        return waitlist


class ProcessWaitlistService:
    """Service for processing waitlist and promoting users."""
    
    def execute(self, event_id: uuid.UUID, available_spots: int) -> List[Waitlist]:
        """Promote users from waitlist to registration."""
        if available_spots <= 0:
            return []
        
        # Get waitlist entries ordered by priority then position
        waitlist_entries = Waitlist.objects.filter(
            event_id=event_id,
            is_promoted=False
        ).order_by('-priority', 'position')[:available_spots]
        
        promoted = []
        for entry in waitlist_entries:
            entry.promote()
            promoted.append(entry)
        
        return promoted


class GetWaitlistPositionService:
    """Service for getting user's waitlist position."""
    
    def execute(self, event_id: uuid.UUID, user_id: uuid.UUID) -> Dict[str, Any]:
        """Get waitlist position for user."""
        try:
            waitlist = Waitlist.objects.get(
                event_id=event_id,
                user_id=user_id,
                is_promoted=False
            )
            
            # Count users ahead
            ahead = Waitlist.objects.filter(
                event_id=event_id,
                is_promoted=False,
                position__lt=waitlist.position
            ).count()
            
            return {
                'position': waitlist.position,
                'users_ahead': ahead,
                'joined_at': waitlist.joined_at,
            }
        except Waitlist.DoesNotExist:
            raise ValidationError('Not on waitlist')
