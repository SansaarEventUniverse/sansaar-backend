import pytest
from django.core.exceptions import ValidationError

from application.update_profile_service import UpdateProfileService
from domain.user_profile_model import UserProfile


@pytest.mark.django_db
class TestUpdateProfileService:
    def setup_method(self):
        self.service = UpdateProfileService()
        self.profile = UserProfile.objects.create(
            user_id='123',
            email='test@example.com',
            first_name='John',
            last_name='Doe'
        )

    def test_update_profile_success(self):
        result = self.service.update_profile(
            user_id='123',
            first_name='Jane',
            last_name='Smith',
            bio='Developer'
        )

        assert result.first_name == 'Jane'
        assert result.last_name == 'Smith'
        assert result.bio == 'Developer'

    def test_update_profile_not_found(self):
        with pytest.raises(ValidationError, match='Profile not found'):
            self.service.update_profile('nonexistent', first_name='Jane')

    def test_update_profile_bio_too_long(self):
        with pytest.raises(ValidationError):
            self.service.update_profile('123', bio='a' * 501)
