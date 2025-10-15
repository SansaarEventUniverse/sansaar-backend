import pytest

from domain.mfa_secret_model import MFASecret
from domain.user_model import User


@pytest.mark.django_db
class TestMFASecretModel:
    def setup_method(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="Password@123", first_name="Test", last_name="User"
        )

    def test_create_mfa_secret(self):
        secret = MFASecret.objects.create(user=self.user, secret="JBSWY3DPEHPK3PXP")

        assert secret.user == self.user
        assert secret.secret == "JBSWY3DPEHPK3PXP"
        assert secret.is_verified is False

    def test_verify_mfa_secret(self):
        secret = MFASecret.objects.create(user=self.user, secret="JBSWY3DPEHPK3PXP")

        secret.verify()

        assert secret.is_verified is True

    def test_one_secret_per_user(self):
        MFASecret.objects.create(user=self.user, secret="JBSWY3DPEHPK3PXP")

        # Creating another secret should fail
        with pytest.raises(Exception):
            MFASecret.objects.create(user=self.user, secret="ANOTHER_SECRET")
