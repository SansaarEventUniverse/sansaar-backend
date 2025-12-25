from domain.models import APIUsage


class APIAnalyticsService:
    def get_endpoint_analytics(self, endpoint: str):
        usage_records = APIUsage.objects.filter(endpoint=endpoint)
        if not usage_records.exists():
            return None
        
        total = usage_records.count()
        successful = usage_records.filter(status_code__gte=200, status_code__lt=300).count()
        
        return {
            "endpoint": endpoint,
            "total_requests": total,
            "successful_requests": successful,
            "failed_requests": total - successful
        }
