from typing import Dict, Any
import uuid
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.utils import timezone

from domain.group_registration import GroupRegistration, GroupMember


class CreateGroupRegistrationService:
    """Service for creating group registrations."""
    
    def execute(self, data: Dict[str, Any]) -> GroupRegistration:
        """Create a group registration."""
        group = GroupRegistration(
            event_id=uuid.UUID(data['event_id']),
            group_name=data['group_name'],
            group_leader_id=uuid.UUID(data['group_leader_id']),
            group_leader_email=data['group_leader_email'],
            min_size=data.get('min_size', 2),
            max_size=data['max_size'],
            price_per_person=Decimal(str(data.get('price_per_person', 0))),
        )
        group.clean()
        group.save()
        return group


class AddGroupMemberService:
    """Service for adding members to group."""
    
    def execute(self, group_id: uuid.UUID, user_id: uuid.UUID, 
                name: str, email: str) -> GroupMember:
        """Add a member to group."""
        try:
            group = GroupRegistration.objects.get(id=group_id)
        except GroupRegistration.DoesNotExist:
            raise ValidationError('Group not found')
        
        if group.is_full():
            raise ValidationError('Group is full')
        
        if group.status == 'cancelled':
            raise ValidationError('Cannot join cancelled group')
        
        # Check duplicate
        if GroupMember.objects.filter(group=group, user_id=user_id).exists():
            raise ValidationError('User already in group')
        
        member = GroupMember.objects.create(
            group=group,
            user_id=user_id,
            name=name,
            email=email,
        )
        
        # Update group size
        group.current_size += 1
        group.calculate_total()
        group.save()
        
        return member


class ConfirmGroupRegistrationService:
    """Service for confirming group registration."""
    
    def execute(self, group_id: uuid.UUID) -> GroupRegistration:
        """Confirm group registration."""
        try:
            group = GroupRegistration.objects.get(id=group_id)
        except GroupRegistration.DoesNotExist:
            raise ValidationError('Group not found')
        
        if group.current_size < group.min_size:
            raise ValidationError(f'Group needs at least {group.min_size} members')
        
        group.status = 'confirmed'
        group.save()
        return group


class CancelGroupRegistrationService:
    """Service for cancelling group registration."""
    
    def execute(self, group_id: uuid.UUID) -> GroupRegistration:
        """Cancel group registration."""
        try:
            group = GroupRegistration.objects.get(id=group_id)
        except GroupRegistration.DoesNotExist:
            raise ValidationError('Group not found')
        
        group.status = 'cancelled'
        group.cancelled_at = timezone.now()
        group.save()
        return group
