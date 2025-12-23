from domain.models import AuditTrail


class AuditLogger:
    def log(self, user_id: str, action: str, resource: str, status: str = "success"):
        return AuditTrail.objects.create(
            user_id=user_id,
            action=action,
            resource=resource,
            status=status
        )
