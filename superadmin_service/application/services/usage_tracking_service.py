from domain.models import APIUsage


class UsageTrackingService:
    def track_request(self, endpoint: str, method: str, status_code: int, response_time: float):
        return APIUsage.objects.create(
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            response_time=response_time
        )

    def get_usage_stats(self, endpoint: str):
        usage_records = APIUsage.objects.filter(endpoint=endpoint)
        return {
            "endpoint": endpoint,
            "total_requests": usage_records.count()
        }
