from datetime import UTC, datetime, timedelta

import jwt
from django.conf import settings
from django.core.cache import cache


class JWTService:
    def generate_token(self, admin_id: str, email: str) -> str:
        payload = {
            "admin_id": admin_id,
            "email": email,
            "exp": datetime.now(UTC) + timedelta(hours=settings.SUPERADMIN_JWT_EXPIRY_HOURS),
            "iat": datetime.now(UTC),
        }
        return jwt.encode(payload, settings.SUPERADMIN_JWT_SECRET, algorithm=settings.SUPERADMIN_JWT_ALGORITHM)

    def verify_token(self, token: str) -> dict:
        if self.is_blacklisted(token):
            raise jwt.InvalidTokenError("Token has been blacklisted")

        try:
            payload = jwt.decode(token, settings.SUPERADMIN_JWT_SECRET, algorithms=[settings.SUPERADMIN_JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise jwt.InvalidTokenError("Token has expired")
        except jwt.InvalidTokenError:
            raise jwt.InvalidTokenError("Invalid token")

    def blacklist_token(self, token: str):
        try:
            payload = jwt.decode(token, settings.SUPERADMIN_JWT_SECRET, algorithms=[settings.SUPERADMIN_JWT_ALGORITHM])
            exp = payload.get("exp")
            if exp:
                ttl = exp - int(datetime.now(UTC).timestamp())
                if ttl > 0:
                    cache.set(f"blacklist:{token}", True, timeout=ttl)
        except jwt.InvalidTokenError:
            pass

    def is_blacklisted(self, token: str) -> bool:
        return cache.get(f"blacklist:{token}") is not None
