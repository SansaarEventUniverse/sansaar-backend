from django.db import models

from domain.user_model import User


class BackupCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="backup_codes")
    code = models.CharField(max_length=20, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "backup_codes"
        indexes = [
            models.Index(fields=["user", "is_used"]),
        ]

    def __str__(self):
        return f"Backup Code for {self.user.email}"

    def mark_as_used(self):
        from django.utils import timezone

        self.is_used = True
        self.used_at = timezone.now()
        self.save()
