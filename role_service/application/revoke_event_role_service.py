from domain.event_role_model import EventRole


class RevokeEventRoleService:
    def execute(self, event_id, user_id):
        try:
            role = EventRole.objects.get(
                event_id=event_id,
                user_id=user_id,
                is_active=True
            )
            role.revoke()
            return True
        except EventRole.DoesNotExist:
            return False
