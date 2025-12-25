from django.db import models


class APIUsage(models.Model):
    endpoint = models.CharField(max_length=200)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField()
    response_time = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'api_usage'
        indexes = [models.Index(fields=['endpoint', 'timestamp'])]

    def is_successful(self):
        return 200 <= self.status_code < 300


class APIMetrics(models.Model):
    endpoint = models.CharField(max_length=200)
    total_requests = models.IntegerField(default=0)
    successful_requests = models.IntegerField(default=0)
    failed_requests = models.IntegerField(default=0)
    avg_response_time = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'api_metrics'
        indexes = [models.Index(fields=['endpoint', 'created_at'])]

    def success_rate(self):
        if self.total_requests == 0:
            return 0.0
        return (self.successful_requests / self.total_requests) * 100
