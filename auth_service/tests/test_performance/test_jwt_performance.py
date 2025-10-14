import time

import pytest

from domain.user_model import User
from infrastructure.services.jwt_service import JWTService


@pytest.mark.django_db
class TestJWTPerformance:
    def setup_method(self):
        self.jwt_service = JWTService()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='Password@123',
            first_name='Test',
            last_name='User'
        )

    def test_token_generation_performance(self):
        """Test that token generation is fast (< 100ms for 100 tokens)"""
        start_time = time.time()

        for _ in range(100):
            self.jwt_service.generate_access_token(self.user)

        elapsed_time = time.time() - start_time
        assert elapsed_time < 0.1, f"Token generation took {elapsed_time}s, expected < 0.1s"

    def test_token_verification_performance(self):
        """Test that token verification is fast (< 100ms for 100 verifications)"""
        token = self.jwt_service.generate_access_token(self.user)

        start_time = time.time()

        for _ in range(100):
            self.jwt_service.decode_token(token)

        elapsed_time = time.time() - start_time
        assert elapsed_time < 0.1, f"Token verification took {elapsed_time}s, expected < 0.1s"

    def test_password_hashing_performance(self):
        """Test that password hashing is reasonable (< 1s for 10 hashes)"""
        start_time = time.time()

        for i in range(10):
            User.objects.create_user(
                email=f'user{i}@example.com',
                password='Password@123',
                first_name='Test',
                last_name='User'
            )

        elapsed_time = time.time() - start_time
        assert elapsed_time < 1.0, f"Password hashing took {elapsed_time}s, expected < 1.0s"
