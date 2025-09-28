from django.core.exceptions import ValidationError


class DisableMFAService:
    def disable_mfa(self, user):
        if not hasattr(user, 'mfa_secret'):
            raise ValidationError('MFA not enabled')

        user.mfa_secret.delete()
        user.backup_codes.all().delete()

        return True
