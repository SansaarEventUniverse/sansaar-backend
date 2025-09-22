
from domain.password_reset_token_model import PasswordResetToken
from domain.user_model import User
from infrastructure.services.email_service import EmailService


class RequestPasswordResetService:
    def request_reset(self, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Don't reveal if email exists
            return True

        # Delete old tokens
        PasswordResetToken.objects.filter(user=user).delete()

        # Create new token
        token = PasswordResetToken.objects.create(user=user)

        # Send email
        email_service = EmailService()
        email_service.send_password_reset_email(
            to_email=user.email,
            reset_token=token.token,
            first_name=user.first_name
        )

        return True
