import uuid

import pyotp
from django.core.exceptions import ValidationError
from django.db import models


class SuperAdmin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    mfa_secret = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "superadmins"

    def verify_mfa(self, token: str) -> bool:
        if not self.mfa_secret:
            raise ValidationError("MFA not configured")
        totp = pyotp.TOTP(self.mfa_secret)
        return totp.verify(token)

    def generate_mfa_secret(self) -> str:
        self.mfa_secret = pyotp.random_base32()
        self.save(update_fields=["mfa_secret"])
        return self.mfa_secret

    def get_mfa_uri(self, issuer: str = "SansaarEventUniverse") -> str:
        if not self.mfa_secret:
            raise ValidationError("MFA not configured")
        totp = pyotp.TOTP(self.mfa_secret)
        return totp.provisioning_uri(name=self.email, issuer_name=issuer)

    def validate_active(self):
        if not self.is_active:
            raise ValidationError("SuperAdmin account is inactive")

    def __str__(self):
        return self.email
