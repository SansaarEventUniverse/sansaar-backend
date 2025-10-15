import re

from django.core.exceptions import ValidationError


class ChangePasswordService:
    def change_password(self, user, current_password, new_password):
        if not user.check_password(current_password):
            raise ValidationError("Current password is incorrect")

        if current_password == new_password:
            raise ValidationError("New password must be different from current password")

        # Check password history
        if user.has_used_password(new_password):
            raise ValidationError("Password was used recently. Please choose a different password")

        self._validate_password(new_password)

        # Save old password to history
        old_password_hash = user.password
        user.set_password(new_password)
        user.save()
        user.add_password_to_history(old_password_hash)

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
