import json
from datetime import timedelta

import boto3
from decouple import config
from django.utils import timezone

from domain.models import AuditLog
from infrastructure.retention_policy import AuditLogRetentionPolicy


class AuditLogArchivalService:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
            region_name=config("AWS_REGION"),
        )
        self.bucket_name = config("AUDIT_LOG_BUCKET", default="sansaar-audit-logs")

    def archive_logs(self, logs):
        if not logs:
            return 0

        archived_count = 0
        for log in logs:
            try:
                key = f"archived/{log.event_type}/{log.created_at.year}/{log.created_at.month}/{log.id}.json"
                data = {
                    "id": log.id,
                    "event_type": log.event_type,
                    "user_id": log.user_id,
                    "ip_address": log.ip_address,
                    "user_agent": log.user_agent,
                    "success": log.success,
                    "metadata": log.metadata,
                    "created_at": log.created_at.isoformat(),
                }

                self.s3_client.put_object(
                    Bucket=self.bucket_name, Key=key, Body=json.dumps(data), StorageClass="GLACIER"
                )
                archived_count += 1
            except Exception:
                continue

        return archived_count

    def get_logs_for_archival(self):
        cutoff_date = timezone.now() - timedelta(days=90)
        return AuditLog.objects.filter(created_at__lt=cutoff_date).order_by("created_at")[:1000]

    def get_logs_for_deletion(self):
        logs_to_delete = []
        for event_type, retention_period in AuditLogRetentionPolicy.RETENTION_PERIODS.items():
            cutoff_date = timezone.now() - retention_period
            logs = AuditLog.objects.filter(event_type=event_type, created_at__lt=cutoff_date)
            logs_to_delete.extend(logs)
        return logs_to_delete

    def delete_logs(self, log_ids):
        if not log_ids:
            return 0
        return AuditLog.objects.filter(id__in=log_ids).delete()[0]
