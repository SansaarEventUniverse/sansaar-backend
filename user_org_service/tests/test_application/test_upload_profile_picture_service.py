from unittest.mock import Mock, patch

import pytest
from django.core.exceptions import ValidationError

from application.upload_profile_picture_service import UploadProfilePictureService
from domain.user_profile_model import UserProfile


@pytest.mark.django_db
class TestUploadProfilePictureService:
    def setup_method(self):
        self.profile = UserProfile.objects.create(
            user_id="123", email="test@example.com", first_name="John", last_name="Doe"
        )

    @patch("application.upload_profile_picture_service.S3Service")
    def test_upload_profile_picture_success(self, mock_s3_class):
        mock_s3_instance = Mock()
        mock_s3_instance.upload_profile_picture.return_value = "https://example.com/profile.jpg"
        mock_s3_class.return_value = mock_s3_instance

        service = UploadProfilePictureService()

        file = Mock()
        file.size = 1024 * 1024  # 1MB
        file.name = "profile.jpg"

        result = service.upload("123", file)

        assert result.profile_picture_url == "https://example.com/profile.jpg"
        mock_s3_instance.upload_profile_picture.assert_called_once_with(file, "123")

    def test_upload_profile_picture_file_too_large(self):
        service = UploadProfilePictureService()
        file = Mock()
        file.size = 6 * 1024 * 1024  # 6MB

        with pytest.raises(ValidationError, match="File size must not exceed 5MB"):
            service.upload("123", file)

    def test_upload_profile_picture_not_found(self):
        service = UploadProfilePictureService()
        file = Mock()
        file.size = 1024

        with pytest.raises(ValidationError, match="Profile not found"):
            service.upload("nonexistent", file)
