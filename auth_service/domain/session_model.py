from django.db import models
from django.utils import timezone

from domain.user_model import User


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    device_type = models.CharField(max_length=50, null=True, blank=True)
    browser = models.CharField(max_length=50, null=True, blank=True)
    os = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    last_activity_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    revoked_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sessions"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["is_active", "expires_at"]),
        ]

    def __str__(self):
        return f"Session for {self.user.email} from {self.ip_address}"

    def save(self, *args, **kwargs):
        if not self.expires_at:
            # Default expiry: 30 days
            self.expires_at = timezone.now() + timezone.timedelta(days=30)
        super().save(*args, **kwargs)

    def is_expired(self):
        """Check if session has expired"""
        return timezone.now() > self.expires_at

    def revoke(self):
        """Revoke the session"""
        self.is_active = False
        self.revoked_at = timezone.now()
        self.save()

    def update_last_activity(self):
        """Update last activity timestamp"""
        self.last_activity_at = timezone.now()
        self.save()
