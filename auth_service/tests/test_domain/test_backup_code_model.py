import pytest

from domain.backup_code_model import BackupCode
from domain.user_model import User


@pytest.mark.django_db
class TestBackupCodeModel:
    def setup_method(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='Password@123',
            first_name='Test',
            last_name='User'
        )

    def test_create_backup_code(self):
        code = BackupCode.objects.create(
            user=self.user,
            code='ABC123DEF456'
        )

        assert code.user == self.user
        assert code.code == 'ABC123DEF456'
        assert code.is_used is False

    def test_use_backup_code(self):
        code = BackupCode.objects.create(
            user=self.user,
            code='ABC123DEF456'
        )

        code.mark_as_used()

        assert code.is_used is True
        assert code.used_at is not None

    def test_cannot_reuse_backup_code(self):
        code = BackupCode.objects.create(
            user=self.user,
            code='ABC123DEF456'
        )

        code.mark_as_used()

        # Should not be able to use again
        assert code.is_used is True
