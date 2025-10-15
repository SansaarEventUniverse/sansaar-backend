from celery import shared_task

from infrastructure.services.audit_log_archival_service import AuditLogArchivalService


@shared_task
def archive_audit_logs():
    service = AuditLogArchivalService()
    logs = service.get_logs_for_archival()
    archived_count = service.archive_logs(logs)

    if archived_count > 0:
        log_ids = [log.id for log in logs[:archived_count]]
        service.delete_logs(log_ids)

    return {"archived": archived_count, "deleted": archived_count}


@shared_task
def delete_expired_audit_logs():
    service = AuditLogArchivalService()
    logs = service.get_logs_for_deletion()
    log_ids = [log.id for log in logs]
    deleted_count = service.delete_logs(log_ids)
    return {"deleted": deleted_count}
