from domain.models import APIMetrics


class APIMonitoringService:
    def get_all_metrics(self):
        return list(APIMetrics.objects.all().order_by('-created_at'))
