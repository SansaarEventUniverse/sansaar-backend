from django.db import models


class AuditEventType:
    REGISTRATION = "REGISTRATION"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    EMAIL_VERIFICATION = "EMAIL_VERIFICATION"
    PASSWORD_RESET = "PASSWORD_RESET"
    PASSWORD_CHANGE = "PASSWORD_CHANGE"
    ACCOUNT_LOCKED = "ACCOUNT_LOCKED"
    SESSION_CREATED = "SESSION_CREATED"
    SESSION_REVOKED = "SESSION_REVOKED"
    ACCOUNT_ANONYMIZED = "ACCOUNT_ANONYMIZED"

    CHOICES = [
        (REGISTRATION, "Registration"),
        (LOGIN, "Login"),
        (LOGOUT, "Logout"),
        (EMAIL_VERIFICATION, "Email Verification"),
        (PASSWORD_RESET, "Password Reset"),
        (PASSWORD_CHANGE, "Password Change"),
        (ACCOUNT_LOCKED, "Account Locked"),
        (SESSION_CREATED, "Session Created"),
        (SESSION_REVOKED, "Session Revoked"),
        (ACCOUNT_ANONYMIZED, "Account Anonymized"),
    ]


class AuditLog(models.Model):
    event_type = models.CharField(max_length=50, choices=AuditEventType.CHOICES)
    user_id = models.CharField(max_length=255, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    success = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "audit_logs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["event_type", "created_at"]),
            models.Index(fields=["user_id", "created_at"]),
        ]

    def __str__(self):
        return f"{self.event_type} - {self.user_id} - {self.created_at}"

    def get_event_description(self):
        status = "successful" if self.success else "failed"
        return f"{self.event_type} event for user {self.user_id} ({status})"
