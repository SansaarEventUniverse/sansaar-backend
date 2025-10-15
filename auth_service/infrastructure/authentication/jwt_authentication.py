from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from domain.user_model import User
from infrastructure.services.jwt_service import JWTService


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        try:
            token_type, token = auth_header.split()
            if token_type.lower() != "bearer":
                return None

            jwt_service = JWTService()
            payload = jwt_service.decode_token(token)

            user = User.objects.get(id=payload["user_id"])
            return (user, None)
        except (ValueError, User.DoesNotExist):
            raise AuthenticationFailed("Invalid token")
        except Exception:
            raise AuthenticationFailed("Authentication failed")
