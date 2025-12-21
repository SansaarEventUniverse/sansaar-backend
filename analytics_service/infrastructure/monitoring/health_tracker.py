from domain.models import SystemHealth


class HealthTracker:
    def track(self, service_name: str, cpu_usage: float, memory_usage: float):
        status = "healthy" if cpu_usage < 80 and memory_usage < 80 else "critical"
        return SystemHealth.objects.create(
            service_name=service_name,
            status=status,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage
        )
