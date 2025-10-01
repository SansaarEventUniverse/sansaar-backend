from django.db import models
from django.utils import timezone

from domain.user_model import User

LOCKOUT_THRESHOLD = 5
LOCKOUT_DURATION = 15  # minutes


class LoginAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_attempts')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'login_attempts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"Login attempt for {self.user.email} at {self.created_at}"
