from datetime import timedelta


class AuditLogRetentionPolicy:
    # Retention periods by event type
    RETENTION_PERIODS = {
        "REGISTRATION": timedelta(days=2555),  # 7 years
        "LOGIN": timedelta(days=90),
        "LOGOUT": timedelta(days=90),
        "EMAIL_VERIFICATION": timedelta(days=365),
        "PASSWORD_RESET": timedelta(days=365),
        "PASSWORD_CHANGE": timedelta(days=365),
        "ACCOUNT_LOCKED": timedelta(days=730),  # 2 years
        "SESSION_CREATED": timedelta(days=90),
        "SESSION_REVOKED": timedelta(days=90),
        "ACCOUNT_ANONYMIZED": timedelta(days=2555),  # 7 years
    }

    DEFAULT_RETENTION = timedelta(days=365)

    @classmethod
    def get_retention_period(cls, event_type: str) -> timedelta:
        return cls.RETENTION_PERIODS.get(event_type, cls.DEFAULT_RETENTION)
