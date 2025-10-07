from django.core.exceptions import ValidationError

from domain.event_role_model import EventRole


class AssignEventRoleService:
    def execute(self, event_id, user_id, role):
        if EventRole.objects.filter(event_id=event_id, user_id=user_id, is_active=True).exists():
            raise ValidationError('User already has an active role in this event')
        
        event_role = EventRole.objects.create(
            event_id=event_id,
            user_id=user_id,
            role=role
        )
        
        return event_role
