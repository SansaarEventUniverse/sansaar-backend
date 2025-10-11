import jwt
import pytest
from django.core.cache import cache

from infrastructure.services.jwt_service import JWTService


class TestJWTService:
    def setup_method(self):
        cache.clear()

    def test_generate_token(self):
        service = JWTService()
        token = service.generate_token("admin-123", "admin@example.com")
        assert token is not None
        assert isinstance(token, str)

    def test_verify_token_valid(self):
        service = JWTService()
        token = service.generate_token("admin-123", "admin@example.com")
        payload = service.verify_token(token)
        assert payload["admin_id"] == "admin-123"
        assert payload["email"] == "admin@example.com"

    def test_verify_token_invalid(self):
        service = JWTService()
        with pytest.raises(jwt.InvalidTokenError):
            service.verify_token("invalid_token")

    def test_blacklist_token(self):
        service = JWTService()
        token = service.generate_token("admin-123", "admin@example.com")
        service.blacklist_token(token)
        assert service.is_blacklisted(token) is True

    def test_verify_blacklisted_token(self):
        service = JWTService()
        token = service.generate_token("admin-123", "admin@example.com")
        service.blacklist_token(token)
        with pytest.raises(jwt.InvalidTokenError, match="Token has been blacklisted"):
            service.verify_token(token)

    def test_is_blacklisted_false(self):
        service = JWTService()
        token = service.generate_token("admin-123", "admin@example.com")
        assert service.is_blacklisted(token) is False
