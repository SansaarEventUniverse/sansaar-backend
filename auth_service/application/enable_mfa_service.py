import secrets

import pyotp

from domain.backup_code_model import BackupCode
from domain.mfa_secret_model import MFASecret


class EnableMFAService:
    def enable_mfa(self, user):
        # Generate secret
        secret = pyotp.random_base32()

        # Create or update MFA secret
        mfa_secret, created = MFASecret.objects.get_or_create(user=user, defaults={"secret": secret})
        if not created:
            mfa_secret.secret = secret
            mfa_secret.is_verified = False
            mfa_secret.save()

        # Generate QR code data
        totp = pyotp.TOTP(secret)
        qr_code_data = totp.provisioning_uri(name=user.email, issuer_name="Sansaar Event Universe")

        # Generate backup codes
        backup_codes = []
        BackupCode.objects.filter(user=user).delete()  # Remove old codes

        for _ in range(10):
            code = secrets.token_hex(6).upper()
            BackupCode.objects.create(user=user, code=code)
            backup_codes.append(code)

        return {"secret": secret, "qr_code_data": qr_code_data, "backup_codes": backup_codes}
