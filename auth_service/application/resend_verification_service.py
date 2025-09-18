from django.core.exceptions import ValidationError

from domain.email_verification_token_model import EmailVerificationToken
from domain.user_model import User
from infrastructure.services.email_service import EmailService


class ResendVerificationService:
    def resend(self, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError('User not found')

        if user.is_email_verified:
            raise ValidationError('Email already verified')

        # Delete old tokens
        EmailVerificationToken.objects.filter(user=user).delete()

        # Create new token
        token = EmailVerificationToken.objects.create(user=user)

        # Send email
        email_service = EmailService()
        email_service.send_verification_email(
            to_email=user.email,
            verification_token=token.token,
            first_name=user.first_name
        )

        return True
