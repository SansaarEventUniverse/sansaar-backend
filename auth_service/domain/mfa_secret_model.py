from django.db import models

from domain.user_model import User


class MFASecret(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="mfa_secret")
    secret = models.CharField(max_length=32)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "mfa_secrets"

    def __str__(self):
        return f"MFA Secret for {self.user.email}"

    def verify(self):
        from django.utils import timezone

        self.is_verified = True
        self.verified_at = timezone.now()
        self.save()
