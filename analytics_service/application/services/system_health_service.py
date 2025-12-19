from domain.models import SystemHealth


class SystemHealthService:
    def check_health(self, service_name: str, cpu_usage: float, memory_usage: float):
        status = "healthy"
        if cpu_usage > 80 or memory_usage > 80:
            status = "critical"
        
        return SystemHealth.objects.create(
            service_name=service_name,
            status=status,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage
        )

    def get_critical_services(self):
        return list(SystemHealth.objects.filter(status="critical"))
