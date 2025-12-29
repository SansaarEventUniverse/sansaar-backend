from domain.models import SecurityEvent


class ThreatDetector:
    def detect_threats(self):
        return list(SecurityEvent.objects.filter(severity__in=["high", "critical"]))
