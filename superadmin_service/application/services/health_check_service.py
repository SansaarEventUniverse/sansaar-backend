from domain.models import HealthCheck


class HealthCheckService:
    def perform_check(self, service_name: str, endpoint: str, status: str, response_time: float):
        return HealthCheck.objects.create(
            service_name=service_name,
            endpoint=endpoint,
            status=status,
            response_time=response_time
        )

    def get_recent_checks(self, service_name: str, limit: int = 10):
        return list(HealthCheck.objects.filter(service_name=service_name).order_by('-checked_at')[:limit])
