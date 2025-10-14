from domain.audit_log_model import AuditLog


class LogAuditEventService:
    def log_event(self, event_type, user_id, ip_address=None, user_agent=None, success=True, metadata=None):
        AuditLog.objects.create(
            event_type=event_type,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
            metadata=metadata or {}
        )
