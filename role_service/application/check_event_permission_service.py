from domain.event_role_model import EventRole
from domain.permission_model import Permission


class CheckEventPermissionService:
    def execute(self, event_id, user_id, resource, action):
        try:
            role = EventRole.objects.get(
                event_id=event_id,
                user_id=user_id,
                is_active=True
            )
            
            return Permission.objects.filter(
                role=role.role,
                resource=resource,
                action=action
            ).exists()
        except EventRole.DoesNotExist:
            return False
