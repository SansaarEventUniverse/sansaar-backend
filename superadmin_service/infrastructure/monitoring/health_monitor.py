from domain.models import SystemHealth, HealthCheck
import psutil


class HealthMonitor:
    def monitor_service(self, service_name: str):
        cpu_usage = psutil.cpu_percent(interval=0.1)
        memory_usage = psutil.virtual_memory().percent
        status = self._determine_status(cpu_usage, memory_usage)
        
        return SystemHealth.objects.create(
            service_name=service_name,
            status=status,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage
        )

    def check_service_endpoint(self, service_name: str, endpoint: str):
        status = "healthy"
        response_time = 0.1
        
        return HealthCheck.objects.create(
            service_name=service_name,
            endpoint=endpoint,
            status=status,
            response_time=response_time
        )

    def _determine_status(self, cpu_usage: float, memory_usage: float):
        if cpu_usage > 90 or memory_usage > 90:
            return "critical"
        elif cpu_usage > 75 or memory_usage > 75:
            return "warning"
        return "healthy"
