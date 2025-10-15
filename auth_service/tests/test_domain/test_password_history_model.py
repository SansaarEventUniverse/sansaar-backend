import pytest

from domain.password_history_model import PasswordHistory
from domain.user_model import User


@pytest.mark.django_db
class TestPasswordHistoryModel:
    def setup_method(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="Password@123", first_name="Test", last_name="User"
        )

    def test_create_password_history(self):
        history = PasswordHistory.objects.create(user=self.user, password_hash="hashed_password")

        assert history.user == self.user
        assert history.password_hash == "hashed_password"

    def test_password_history_ordering(self):
        # Create multiple history entries
        PasswordHistory.objects.create(user=self.user, password_hash="hash1")
        PasswordHistory.objects.create(user=self.user, password_hash="hash2")
        PasswordHistory.objects.create(user=self.user, password_hash="hash3")

        histories = PasswordHistory.objects.filter(user=self.user)

        # Should be ordered by created_at descending (newest first)
        assert histories[0].password_hash == "hash3"
        assert histories[1].password_hash == "hash2"
        assert histories[2].password_hash == "hash1"

    def test_user_has_used_password(self):
        # Add password to history
        PasswordHistory.objects.create(user=self.user, password_hash=self.user.password)

        # Check if password was used
        assert self.user.has_used_password("Password@123") is True
        assert self.user.has_used_password("DifferentPassword@456") is False

    def test_add_password_to_history(self):
        old_password = self.user.password

        # Change password
        self.user.set_password("NewPassword@456")
        self.user.save()

        # Add old password to history
        self.user.add_password_to_history(old_password)

        assert PasswordHistory.objects.filter(user=self.user).count() == 1
        assert self.user.has_used_password("Password@123") is True
