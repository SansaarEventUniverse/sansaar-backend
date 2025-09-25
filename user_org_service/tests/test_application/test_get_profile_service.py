import pytest
from django.core.exceptions import ValidationError

from application.get_profile_service import GetProfileService
from domain.user_profile_model import UserProfile


@pytest.mark.django_db
class TestGetProfileService:
    def setup_method(self):
        self.service = GetProfileService()

    def test_get_profile_success(self):
        UserProfile.objects.create(
            user_id='123',
            email='test@example.com',
            first_name='John',
            last_name='Doe'
        )

        result = self.service.get_profile('123')

        assert result.user_id == '123'
        assert result.email == 'test@example.com'

    def test_get_profile_not_found(self):
        with pytest.raises(ValidationError, match='Profile not found'):
            self.service.get_profile('nonexistent')
