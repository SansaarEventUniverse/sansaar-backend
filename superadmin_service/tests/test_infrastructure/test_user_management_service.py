from unittest.mock import Mock, patch

import pytest
import requests
from django.core.exceptions import ValidationError

from infrastructure.services.user_management_service import UserManagementService


class TestUserManagementService:
    @patch("infrastructure.services.user_management_service.requests.get")
    def test_get_users_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"users": [{"id": "1"}], "total": 1}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        service = UserManagementService()
        result = service.get_users(page=1, limit=50)

        assert result["total"] == 1
        mock_get.assert_called_once()

    @patch("infrastructure.services.user_management_service.requests.get")
    def test_get_users_request_failure(self, mock_get):
        mock_get.side_effect = requests.RequestException("Connection error")

        service = UserManagementService()

        # Now returns empty list instead of raising error
        result = service.get_users()
        assert result["users"] == []
        assert result["total"] == 0

    @patch("infrastructure.services.user_management_service.requests.get")
    def test_get_user_by_id_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"id": "user-123", "email": "user@example.com"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        service = UserManagementService()
        result = service.get_user_by_id("user-123")

        assert result["id"] == "user-123"

    @patch("infrastructure.services.user_management_service.requests.get")
    def test_get_user_by_id_not_found(self, mock_get):
        mock_get.side_effect = requests.RequestException("Not found")

        service = UserManagementService()

        with pytest.raises(ValidationError, match="User not found"):
            service.get_user_by_id("user-123")

    @patch("infrastructure.services.user_management_service.requests.post")
    def test_deactivate_user_success(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"id": "user-123", "is_active": False}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        service = UserManagementService()
        result = service.deactivate_user("user-123")

        assert result["is_active"] is False

    @patch("infrastructure.services.user_management_service.requests.post")
    def test_deactivate_user_failure(self, mock_post):
        mock_post.side_effect = requests.RequestException("Server error")

        service = UserManagementService()

        with pytest.raises(ValidationError, match="User deactivation not implemented"):
            service.deactivate_user("user-123")
