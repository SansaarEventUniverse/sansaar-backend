class AlertThresholds:
    FAILED_LOGIN_ATTEMPTS = 5
    FAILED_LOGIN_WINDOW_MINUTES = 15
    MULTIPLE_LOCATIONS_WINDOW_MINUTES = 30
    PASSWORD_RESET_ATTEMPTS = 3
    PASSWORD_RESET_WINDOW_MINUTES = 60
    ACCOUNT_LOCKOUT_THRESHOLD = 10

    ALERT_TYPES = {
        "FAILED_LOGIN_SPIKE": {"threshold": FAILED_LOGIN_ATTEMPTS, "window_minutes": FAILED_LOGIN_WINDOW_MINUTES},
        "MULTIPLE_LOCATIONS": {"threshold": 2, "window_minutes": MULTIPLE_LOCATIONS_WINDOW_MINUTES},
        "PASSWORD_RESET_SPIKE": {"threshold": PASSWORD_RESET_ATTEMPTS, "window_minutes": PASSWORD_RESET_WINDOW_MINUTES},
        "ACCOUNT_LOCKOUT_SPIKE": {"threshold": ACCOUNT_LOCKOUT_THRESHOLD, "window_minutes": 60},
    }

    @classmethod
    def get_threshold(cls, alert_type: str):
        return cls.ALERT_TYPES.get(alert_type, {"threshold": 5, "window_minutes": 15})
