from domain.models import APIUsage, APIMetrics
from django.db.models import Avg


class MetricsAggregator:
    def aggregate_metrics(self, endpoint: str):
        usage_records = APIUsage.objects.filter(endpoint=endpoint)
        
        total = usage_records.count()
        successful = usage_records.filter(status_code__gte=200, status_code__lt=300).count()
        failed = total - successful
        avg_time = usage_records.aggregate(Avg('response_time'))['response_time__avg'] or 0.0
        
        return APIMetrics.objects.create(
            endpoint=endpoint,
            total_requests=total,
            successful_requests=successful,
            failed_requests=failed,
            avg_response_time=avg_time
        )
