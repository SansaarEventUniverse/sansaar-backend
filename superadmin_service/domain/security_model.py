from django.db import models


class SecurityEvent(models.Model):
    event_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=20)
    source_ip = models.CharField(max_length=45)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'security_events'
        indexes = [models.Index(fields=['severity', 'created_at'])]

    def is_critical(self):
        return self.severity in ["high", "critical"]


class SecurityRule(models.Model):
    name = models.CharField(max_length=200)
    rule_type = models.CharField(max_length=100)
    threshold = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'security_rules'
