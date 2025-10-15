from datetime import timedelta

import pytest
from django.utils import timezone

from domain.user_model import User
from infrastructure.services.jwt_service import JWTService


@pytest.mark.django_db
class TestJWTService:
    def setup_method(self):
        self.service = JWTService()
        self.user = User.objects.create_user(
            email="test@example.com", password="Test@1234", first_name="Test", last_name="User"
        )

    def test_generate_access_token(self):
        token = self.service.generate_access_token(self.user)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_generate_refresh_token(self):
        token = self.service.generate_refresh_token(self.user)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_access_token(self):
        token = self.service.generate_access_token(self.user)
        payload = self.service.decode_token(token)

        assert payload["user_id"] == self.user.id
        assert payload["email"] == self.user.email
        assert "exp" in payload

    def test_decode_expired_token(self):
        # Manually create an expired token for testing

        import jwt
        from django.conf import settings

        payload = {"user_id": self.user.id, "email": self.user.email, "exp": timezone.now() - timedelta(hours=1)}
        expired_token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")

        with pytest.raises(Exception):
            self.service.decode_token(expired_token)

    def test_decode_invalid_token(self):
        with pytest.raises(Exception):
            self.service.decode_token("invalid.token.here")
