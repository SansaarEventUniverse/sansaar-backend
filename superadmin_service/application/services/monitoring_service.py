from domain.models import SystemHealth, HealthCheck


class MonitoringService:
    def get_all_services_health(self):
        return list(SystemHealth.objects.all().order_by('-created_at'))

    def get_critical_services(self):
        return list(SystemHealth.objects.filter(status="critical"))
