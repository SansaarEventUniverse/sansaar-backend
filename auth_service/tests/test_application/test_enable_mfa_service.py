import pytest

from application.enable_mfa_service import EnableMFAService
from domain.user_model import User


@pytest.mark.django_db
class TestEnableMFAService:
    def setup_method(self):
        self.service = EnableMFAService()
        self.user = User.objects.create_user(
            email="test@example.com", password="Password@123", first_name="Test", last_name="User"
        )

    def test_enable_mfa_generates_secret(self):
        result = self.service.enable_mfa(self.user)

        assert "secret" in result
        assert "qr_code_data" in result
        assert len(result["secret"]) == 32  # Base32 secret length

    def test_enable_mfa_creates_backup_codes(self):
        result = self.service.enable_mfa(self.user)

        assert "backup_codes" in result
        assert len(result["backup_codes"]) == 10
