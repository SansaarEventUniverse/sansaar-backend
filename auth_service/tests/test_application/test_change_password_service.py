import pytest
from django.core.exceptions import ValidationError

from application.change_password_service import ChangePasswordService
from domain.user_model import User


@pytest.mark.django_db
class TestChangePasswordService:
    def setup_method(self):
        self.service = ChangePasswordService()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='OldPassword@123',
            first_name='Test',
            last_name='User'
        )

    def test_change_password_success(self):
        result = self.service.change_password(
            user=self.user,
            current_password='OldPassword@123',
            new_password='NewPassword@456'
        )

        assert result is True
        self.user.refresh_from_db()
        assert self.user.check_password('NewPassword@456')

    def test_change_password_wrong_current_password(self):
        with pytest.raises(ValidationError, match='Current password is incorrect'):
            self.service.change_password(
                user=self.user,
                current_password='WrongPassword@123',
                new_password='NewPassword@456'
            )

    def test_change_password_weak_new_password(self):
        with pytest.raises(ValidationError, match='Password must be at least 8 characters'):
            self.service.change_password(
                user=self.user,
                current_password='OldPassword@123',
                new_password='weak'
            )

    def test_change_password_same_as_current(self):
        with pytest.raises(ValidationError, match='New password must be different from current password'):
            self.service.change_password(
                user=self.user,
                current_password='OldPassword@123',
                new_password='OldPassword@123'
            )
