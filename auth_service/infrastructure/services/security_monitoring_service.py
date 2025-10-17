from datetime import timedelta

from django.db.models import Count
from django.utils import timezone

from domain.audit_log_model import AuditEventType
from domain.models import AuditLog
from infrastructure.alert_thresholds import AlertThresholds
from infrastructure.services.alert_service import AlertService


class SecurityMonitoringService:
    def __init__(self):
        self.alert_service = AlertService()
        self.thresholds = AlertThresholds()

    def monitor_failed_logins(self, user_id: str = None):
        threshold_config = self.thresholds.get_threshold("FAILED_LOGIN_SPIKE")
        time_window = timezone.now() - timedelta(minutes=threshold_config["window_minutes"])

        query = AuditLog.objects.filter(
            event_type=AuditEventType.LOGIN, success=False, created_at__gte=time_window
        )

        if user_id:
            query = query.filter(user_id=user_id)
            count = query.count()
            if count >= threshold_config["threshold"]:
                self._trigger_alert(
                    "FAILED_LOGIN_SPIKE",
                    f"User {user_id} has {count} failed login attempts in {threshold_config['window_minutes']} minutes",
                    {"user_id": user_id, "count": count, "window_minutes": threshold_config["window_minutes"]},
                )
                return True
        else:
            user_counts = query.values("user_id").annotate(count=Count("id"))
            for user_count in user_counts:
                if user_count["count"] >= threshold_config["threshold"]:
                    self._trigger_alert(
                        "FAILED_LOGIN_SPIKE",
                        f"User {user_count['user_id']} has {user_count['count']} failed login attempts",
                        {"user_id": user_count["user_id"], "count": user_count["count"]},
                    )
                    return True

        return False

    def monitor_multiple_locations(self, user_id: str):
        threshold_config = self.thresholds.get_threshold("MULTIPLE_LOCATIONS")
        time_window = timezone.now() - timedelta(minutes=threshold_config["window_minutes"])

        logs = AuditLog.objects.filter(
            user_id=user_id, event_type=AuditEventType.LOGIN, success=True, created_at__gte=time_window
        ).values_list("ip_address", flat=True)

        unique_ips = set(filter(None, logs))
        if len(unique_ips) >= threshold_config["threshold"]:
            self._trigger_alert(
                "MULTIPLE_LOCATIONS",
                f"User {user_id} logged in from {len(unique_ips)} different locations",
                {"user_id": user_id, "ip_addresses": list(unique_ips), "count": len(unique_ips)},
            )
            return True

        return False

    def monitor_password_reset_attempts(self, user_id: str = None):
        threshold_config = self.thresholds.get_threshold("PASSWORD_RESET_SPIKE")
        time_window = timezone.now() - timedelta(minutes=threshold_config["window_minutes"])

        query = AuditLog.objects.filter(event_type=AuditEventType.PASSWORD_RESET, created_at__gte=time_window)

        if user_id:
            count = query.filter(user_id=user_id).count()
            if count >= threshold_config["threshold"]:
                self._trigger_alert(
                    "PASSWORD_RESET_SPIKE",
                    f"User {user_id} has {count} password reset attempts",
                    {"user_id": user_id, "count": count},
                )
                return True
        else:
            user_counts = query.values("user_id").annotate(count=Count("id"))
            for user_count in user_counts:
                if user_count["count"] >= threshold_config["threshold"]:
                    self._trigger_alert(
                        "PASSWORD_RESET_SPIKE",
                        f"User {user_count['user_id']} has {user_count['count']} password reset attempts",
                        {"user_id": user_count["user_id"], "count": user_count["count"]},
                    )
                    return True

        return False

    def monitor_account_lockouts(self):
        threshold_config = self.thresholds.get_threshold("ACCOUNT_LOCKOUT_SPIKE")
        time_window = timezone.now() - timedelta(minutes=threshold_config["window_minutes"])

        count = AuditLog.objects.filter(
            event_type=AuditEventType.ACCOUNT_LOCKED, created_at__gte=time_window
        ).count()

        if count >= threshold_config["threshold"]:
            self._trigger_alert(
                "ACCOUNT_LOCKOUT_SPIKE",
                f"{count} accounts locked in {threshold_config['window_minutes']} minutes",
                {"count": count, "window_minutes": threshold_config["window_minutes"]},
            )
            return True

        return False

    def _trigger_alert(self, alert_type: str, message: str, metadata: dict):
        self.alert_service.send_alert(alert_type, message, metadata)
