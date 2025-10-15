import pytest

from domain.user_model import User
from infrastructure.oauth.google_adapter import GoogleOAuthAdapter


@pytest.mark.django_db
class TestGoogleOAuthAdapter:
    def setup_method(self):
        self.adapter = GoogleOAuthAdapter()

    def test_generate_tokens(self):
        user = User.objects.create_user(
            email="test@example.com", password="Test@1234", first_name="Test", last_name="User"
        )

        tokens = self.adapter.generate_tokens(user)

        assert "access_token" in tokens
        assert "refresh_token" in tokens
        assert isinstance(tokens["access_token"], str)
        assert isinstance(tokens["refresh_token"], str)
