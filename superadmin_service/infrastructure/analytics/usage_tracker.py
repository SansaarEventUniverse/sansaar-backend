from domain.models import APIUsage


class UsageTracker:
    def track_api_call(self, endpoint: str, method: str, status_code: int, response_time: float):
        return APIUsage.objects.create(
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            response_time=response_time
        )
