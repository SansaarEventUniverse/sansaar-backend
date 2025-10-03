from datetime import timedelta

import jwt
from django.conf import settings
from django.utils import timezone


class JWTService:
    def generate_access_token(self, user, session_id=None):
        payload = {
            'user_id': user.id,
            'email': user.email,
            'exp': timezone.now() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_LIFETIME // 60)
        }
        if session_id:
            payload['session_id'] = session_id
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')

    def generate_refresh_token(self, user):
        payload = {
            'user_id': user.id,
            'email': user.email,
            'exp': timezone.now() + timedelta(seconds=settings.JWT_REFRESH_TOKEN_LIFETIME)
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')

    def decode_token(self, token):
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
