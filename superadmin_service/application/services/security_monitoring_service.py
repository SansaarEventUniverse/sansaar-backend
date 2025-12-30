from domain.models import SecurityEvent


class SecurityMonitoringService:
    def log_event(self, event_type: str, severity: str, source_ip: str, description: str):
        return SecurityEvent.objects.create(
            event_type=event_type,
            severity=severity,
            source_ip=source_ip,
            description=description
        )

    def get_critical_events(self):
        return list(SecurityEvent.objects.filter(severity__in=["high", "critical"]))
