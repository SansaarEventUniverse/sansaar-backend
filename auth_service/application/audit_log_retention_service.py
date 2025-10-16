from infrastructure.retention_policy import AuditLogRetentionPolicy
from infrastructure.services.audit_log_archival_service import AuditLogArchivalService


class AuditLogRetentionService:
    def __init__(self):
        self.archival_service = AuditLogArchivalService()
        self.retention_policy = AuditLogRetentionPolicy()

    def archive_and_delete_logs(self):
        logs = self.archival_service.get_logs_for_archival()
        if not logs:
            return {"archived": 0, "deleted": 0}

        archived_count = self.archival_service.archive_logs(logs)
        if archived_count > 0:
            log_ids = [log.id for log in logs[:archived_count]]
            deleted_count = self.archival_service.delete_logs(log_ids)
        else:
            deleted_count = 0

        return {"archived": archived_count, "deleted": deleted_count}

    def delete_expired_logs(self):
        logs = self.archival_service.get_logs_for_deletion()
        if not logs:
            return {"deleted": 0}

        log_ids = [log.id for log in logs]
        deleted_count = self.archival_service.delete_logs(log_ids)
        return {"deleted": deleted_count}

    def validate_retention_policy(self, event_type: str):
        retention_period = self.retention_policy.get_retention_period(event_type)
        return {"event_type": event_type, "retention_days": retention_period.days, "valid": True}
