from django.db import models


class Notification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default="unread")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        indexes = [models.Index(fields=['status', 'created_at'])]

    def is_unread(self):
        return self.status == "unread"


class NotificationRule(models.Model):
    name = models.CharField(max_length=200)
    condition = models.CharField(max_length=500)
    notification_type = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notification_rules'
