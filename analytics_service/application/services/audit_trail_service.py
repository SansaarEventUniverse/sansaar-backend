from domain.models import AuditTrail


class AuditTrailService:
    def log_action(self, user_id: str, action: str, resource: str, status: str = "success"):
        return AuditTrail.objects.create(
            user_id=user_id,
            action=action,
            resource=resource,
            status=status
        )

    def get_user_audit_trail(self, user_id: str):
        return list(AuditTrail.objects.filter(user_id=user_id))
