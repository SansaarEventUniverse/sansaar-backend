import secrets
from datetime import timedelta

from django.db import models
from django.utils import timezone


class RefreshToken(models.Model):
    user = models.ForeignKey('domain.User', on_delete=models.CASCADE, related_name='refresh_tokens')
    token = models.CharField(max_length=64, unique=True)
    expires_at = models.DateTimeField()
    is_blacklisted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'refresh_tokens'

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(48)
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def blacklist(self):
        self.is_blacklisted = True
        self.save(update_fields=['is_blacklisted'])

    def __str__(self):
        return f"RefreshToken for {self.user.email}"
