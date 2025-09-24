import pytest
from django.core.exceptions import ValidationError

from domain.user_profile_model import UserProfile


@pytest.mark.django_db
class TestUserProfileModel:
    def test_create_user_profile(self):
        profile = UserProfile.objects.create(
            user_id='123e4567-e89b-12d3-a456-426614174000',
            email='test@example.com',
            first_name='John',
            last_name='Doe'
        )
        
        assert profile.user_id == '123e4567-e89b-12d3-a456-426614174000'
        assert profile.email == 'test@example.com'
        assert profile.first_name == 'John'
        assert profile.last_name == 'Doe'
        assert profile.bio is None
        assert profile.profile_picture_url is None

    def test_update_profile_info(self):
        profile = UserProfile.objects.create(
            user_id='123e4567-e89b-12d3-a456-426614174000',
            email='test@example.com',
            first_name='John',
            last_name='Doe'
        )
        
        profile.update_info(
            first_name='Jane',
            last_name='Smith',
            bio='Software Developer'
        )
        
        assert profile.first_name == 'Jane'
        assert profile.last_name == 'Smith'
        assert profile.bio == 'Software Developer'

    def test_update_profile_picture(self):
        profile = UserProfile.objects.create(
            user_id='123e4567-e89b-12d3-a456-426614174000',
            email='test@example.com',
            first_name='John',
            last_name='Doe'
        )
        
        profile.update_profile_picture('https://example.com/profile.jpg')
        
        assert profile.profile_picture_url == 'https://example.com/profile.jpg'

    def test_bio_max_length_validation(self):
        profile = UserProfile.objects.create(
            user_id='123e4567-e89b-12d3-a456-426614174000',
            email='test@example.com',
            first_name='John',
            last_name='Doe'
        )
        
        long_bio = 'a' * 501
        with pytest.raises(ValidationError):
            profile.update_info(bio=long_bio)

    def test_get_full_name(self):
        profile = UserProfile.objects.create(
            user_id='123e4567-e89b-12d3-a456-426614174000',
            email='test@example.com',
            first_name='John',
            last_name='Doe'
        )
        
        assert profile.get_full_name() == 'John Doe'
