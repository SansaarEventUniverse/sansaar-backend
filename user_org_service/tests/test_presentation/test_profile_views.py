import pytest
from rest_framework import status
from rest_framework.test import APIClient

from domain.user_profile_model import UserProfile


@pytest.mark.django_db
class TestProfileViews:
    def setup_method(self):
        self.client = APIClient()
        self.profile = UserProfile.objects.create(
            user_id="123", email="test@example.com", first_name="John", last_name="Doe", bio="Developer"
        )

    def test_get_profile_success(self):
        response = self.client.get("/api/user-org/profile/123/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["user_id"] == "123"
        assert response.data["email"] == "test@example.com"

    def test_get_profile_not_found(self):
        response = self.client.get("/api/user-org/profile/nonexistent/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_profile_success(self):
        response = self.client.put(
            "/api/user-org/profile/123/update/", {"first_name": "Jane", "last_name": "Smith", "bio": "Engineer"}
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == "Jane"
        assert response.data["last_name"] == "Smith"
        assert response.data["bio"] == "Engineer"

    def test_update_profile_bio_too_long(self):
        response = self.client.put("/api/user-org/profile/123/update/", {"bio": "a" * 501})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_upload_profile_picture_success(self):
        from io import BytesIO
        from unittest.mock import Mock, patch

        with patch("application.upload_profile_picture_service.S3Service") as mock_s3:
            mock_s3_instance = Mock()
            mock_s3_instance.upload_profile_picture.return_value = "https://example.com/profile.jpg"
            mock_s3.return_value = mock_s3_instance

            file = BytesIO(b"test content")
            file.name = "profile.jpg"

            response = self.client.post("/api/user-org/profile/123/picture/", {"file": file}, format="multipart")

            assert response.status_code == status.HTTP_200_OK
            assert "profile_picture_url" in response.data
