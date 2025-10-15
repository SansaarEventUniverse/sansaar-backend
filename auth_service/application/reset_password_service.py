import re

from django.core.exceptions import ValidationError

from domain.password_reset_token_model import PasswordResetToken


class ResetPasswordService:
    def reset_password(self, token_string, new_password):
        try:
            token = PasswordResetToken.objects.select_related("user").get(token=token_string)
        except PasswordResetToken.DoesNotExist:
            raise ValidationError("Invalid or expired token")

        if token.is_expired():
            raise ValidationError("Invalid or expired token")

        user = token.user

        # Check password history
        if user.has_used_password(new_password):
            raise ValidationError("Password was used recently. Please choose a different password")

        # Validate password
        self._validate_password(new_password)

        # Reset password
        old_password_hash = user.password
        user.set_password(new_password)
        user.save()
        user.add_password_to_history(old_password_hash)

        # Delete token
        token.delete()

        return True

    def _validate_password(self, password):
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters")

        if not re.search(r"[A-Z]", password):
            raise ValidationError("Password must contain at least one uppercase letter")

        if not re.search(r"[a-z]", password):
            raise ValidationError("Password must contain at least one lowercase letter")

        if not re.search(r"\d", password):
            raise ValidationError("Password must contain at least one number")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Password must contain at least one special character")
