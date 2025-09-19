from django.core.exceptions import ValidationError

from domain.refresh_token_model import RefreshToken
from domain.user_model import User
from infrastructure.services.jwt_service import JWTService


class LoginService:
    def login(self, email, password):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError('Invalid email or password')

        if not user.check_password(password):
            raise ValidationError('Invalid email or password')

        if not user.is_email_verified:
            raise ValidationError('Email not verified')

        if not user.is_active:
            raise ValidationError('Account is inactive')

        # Generate tokens
        jwt_service = JWTService()
        access_token = jwt_service.generate_access_token(user)
        refresh_token_jwt = jwt_service.generate_refresh_token(user)

        # Store refresh token in database
        RefreshToken.objects.create(user=user)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token_jwt,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }
