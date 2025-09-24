from django.core.exceptions import ValidationError

from domain.refresh_token_model import RefreshToken


class LogoutService:
    def logout(self, refresh_token):
        try:
            token = RefreshToken.objects.get(token=refresh_token)
        except RefreshToken.DoesNotExist:
            raise ValidationError('Invalid refresh token')

        if token.is_blacklisted:
            raise ValidationError('Token already blacklisted')

        if token.is_expired():
            raise ValidationError('Token has expired')

        token.blacklist()
        return True
