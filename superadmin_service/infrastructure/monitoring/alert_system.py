from domain.models import SystemHealth


class AlertSystem:
    def check_critical_services(self):
        critical_services = SystemHealth.objects.filter(status="critical")
        return list(critical_services)
