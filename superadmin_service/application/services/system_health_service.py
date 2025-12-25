from domain.models import SystemHealth


class SystemHealthService:
    def record_health(self, service_name: str, status: str, cpu_usage: float, memory_usage: float):
        return SystemHealth.objects.create(
            service_name=service_name,
            status=status,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage
        )

    def get_service_health(self, service_name: str):
        try:
            return SystemHealth.objects.filter(service_name=service_name).latest('created_at')
        except SystemHealth.DoesNotExist:
            return None
