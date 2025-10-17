from infrastructure.services.security_monitoring_service import SecurityMonitoringService


class SecurityMonitoringApplicationService:
    def __init__(self):
        self.monitoring_service = SecurityMonitoringService()

    def detect_suspicious_activity(self, user_id: str):
        alerts = []

        if self.monitoring_service.monitor_failed_logins(user_id):
            alerts.append("FAILED_LOGIN_SPIKE")

        if self.monitoring_service.monitor_multiple_locations(user_id):
            alerts.append("MULTIPLE_LOCATIONS")

        if self.monitoring_service.monitor_password_reset_attempts(user_id):
            alerts.append("PASSWORD_RESET_SPIKE")

        return {"user_id": user_id, "alerts": alerts, "suspicious": len(alerts) > 0}

    def monitor_system_security(self):
        alerts = []

        if self.monitoring_service.monitor_failed_logins():
            alerts.append("SYSTEM_FAILED_LOGIN_SPIKE")

        if self.monitoring_service.monitor_password_reset_attempts():
            alerts.append("SYSTEM_PASSWORD_RESET_SPIKE")

        if self.monitoring_service.monitor_account_lockouts():
            alerts.append("ACCOUNT_LOCKOUT_SPIKE")

        return {"alerts": alerts, "alert_count": len(alerts)}

    def generate_alert(self, alert_type: str, message: str, metadata: dict = None):
        result = self.monitoring_service.alert_service.send_alert(alert_type, message, metadata)
        return {
            "alert_type": alert_type,
            "message": message,
            "email_sent": result["email_sent"],
            "slack_sent": result["slack_sent"],
        }

    def validate_monitoring_rules(self):
        rules = []
        for alert_type in ["FAILED_LOGIN_SPIKE", "MULTIPLE_LOCATIONS", "PASSWORD_RESET_SPIKE", "ACCOUNT_LOCKOUT_SPIKE"]:
            config = self.monitoring_service.thresholds.get_threshold(alert_type)
            rules.append(
                {
                    "alert_type": alert_type,
                    "threshold": config["threshold"],
                    "window_minutes": config["window_minutes"],
                    "valid": True,
                }
            )
        return {"rules": rules, "total": len(rules)}
