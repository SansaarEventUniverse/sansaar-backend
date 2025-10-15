from django.core.exceptions import ValidationError

from domain.email_verification_token_model import EmailVerificationToken


class VerifyEmailService:
    def verify(self, token_string):
        try:
            token = EmailVerificationToken.objects.select_related("user").get(token=token_string)
        except EmailVerificationToken.DoesNotExist:
            raise ValidationError("Invalid or expired token")

        if token.is_expired():
            raise ValidationError("Invalid or expired token")

        if token.user.is_email_verified:
            raise ValidationError("Email already verified")

        token.user.verify_email()
        token.delete()
        return True
