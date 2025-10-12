from datetime import UTC, datetime

from django.conf import settings
from elasticsearch import Elasticsearch


class AuditLogger:
    def __init__(self):
        self.es = Elasticsearch([f"http://{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}"])
        self.index = "superadmin_audit_logs"

    def log_event(self, event_type: str, admin_id: str, email: str, ip_address: str, metadata: dict = None):
        doc = {
            "event_type": event_type,
            "admin_id": admin_id,
            "email": email,
            "ip_address": ip_address,
            "timestamp": datetime.now(UTC).isoformat(),
            "metadata": metadata or {},
        }

        try:
            self.es.index(index=self.index, document=doc)
        except Exception:
            pass

    def log_superadmin_login(self, admin_id: str, email: str, ip_address: str):
        self.log_event("SUPERADMIN_LOGIN", admin_id, email, ip_address)

    def log_superadmin_logout(self, admin_id: str, email: str, ip_address: str):
        self.log_event("SUPERADMIN_LOGOUT", admin_id, email, ip_address)

    def log_superadmin_login_failed(self, email: str, ip_address: str, reason: str):
        self.log_event("SUPERADMIN_LOGIN_FAILED", "", email, ip_address, {"reason": reason})

    def log_ip_whitelist_violation(self, email: str, ip_address: str):
        self.log_event("IP_WHITELIST_VIOLATION", "", email, ip_address)
