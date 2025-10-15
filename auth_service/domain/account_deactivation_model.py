from datetime import timedelta

from django.db import models
from django.utils import timezone


class AccountDeactivation(models.Model):
    user_id = models.CharField(max_length=255, unique=True, db_index=True)
    deactivated_at = models.DateTimeField(auto_now_add=True)
    grace_period_ends = models.DateTimeField()
    is_permanently_deactivated = models.BooleanField(default=False)
    permanently_deactivated_at = models.DateTimeField(null=True, blank=True)
    is_anonymized = models.BooleanField(default=False)
    anonymized_at = models.DateTimeField(null=True, blank=True)
    reason = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "account_deactivations"
        ordering = ["-deactivated_at"]

    def save(self, *args, **kwargs):
        if not self.grace_period_ends:
            self.grace_period_ends = timezone.now() + timedelta(days=30)
        super().save(*args, **kwargs)

    def is_grace_period_expired(self) -> bool:
        return timezone.now() > self.grace_period_ends

    def can_self_reactivate(self) -> bool:
        """User can reactivate themselves only within grace period"""
        return not self.is_permanently_deactivated and not self.is_grace_period_expired()

    def can_superadmin_reactivate(self) -> bool:
        """SuperAdmin can reactivate unless anonymized"""
        return not self.is_anonymized

    def mark_permanently_deactivated(self):
        self.is_permanently_deactivated = True
        self.permanently_deactivated_at = timezone.now()
        self.save()

    def mark_anonymized(self):
        self.is_anonymized = True
        self.anonymized_at = timezone.now()
        self.save()

    def __str__(self):
        return f"Deactivation for {self.user_id}"
