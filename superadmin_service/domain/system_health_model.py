from django.db import models


class SystemHealth(models.Model):
    service_name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    cpu_usage = models.FloatField(default=0.0)
    memory_usage = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'system_health'
        indexes = [models.Index(fields=['service_name', 'created_at'])]

    def is_critical(self):
        return self.status == "critical"


class HealthCheck(models.Model):
    service_name = models.CharField(max_length=100)
    endpoint = models.CharField(max_length=200)
    status = models.CharField(max_length=50)
    response_time = models.FloatField(default=0.0)
    checked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'health_checks'
        indexes = [models.Index(fields=['service_name', 'checked_at'])]

    def is_healthy(self):
        return self.status == "healthy"
