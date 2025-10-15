import pyotp
from django.core.exceptions import ValidationError


class VerifyMFAService:
    def verify_mfa(self, user, code):
        if not hasattr(user, "mfa_secret"):
            raise ValidationError("MFA not enabled")

        totp = pyotp.TOTP(user.mfa_secret.secret)

        if not totp.verify(code, valid_window=1):
            raise ValidationError("Invalid MFA code")

        # Mark as verified if first time
        if not user.mfa_secret.is_verified:
            user.mfa_secret.verify()

        return True
