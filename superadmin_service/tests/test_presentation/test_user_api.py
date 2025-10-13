from unittest.mock import Mock, patch

from django.test import Client


class TestUserManagementAPI:
    @patch("presentation.views.user_views.UserManagementService")
    def test_list_users_success(self, mock_service_class):
        mock_service = Mock()
        mock_service.get_users.return_value = {
            "users": [
                {
                    "user_id": "1",
                    "email": "user@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "bio": "",
                    "profile_picture_url": None,
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                }
            ],
            "total": 1,
            "page": 1,
            "limit": 50,
        }
        mock_service_class.return_value = mock_service

        client = Client()
        response = client.get("/api/superadmin/users/")

        assert response.status_code == 200
        assert response.json()["total"] == 1

    @patch("presentation.views.user_views.UserManagementService")
    def test_list_users_with_pagination(self, mock_service_class):
        mock_service = Mock()
        mock_service.get_users.return_value = {"users": [], "total": 0, "page": 2, "limit": 10}
        mock_service_class.return_value = mock_service

        client = Client()
        response = client.get("/api/superadmin/users/?page=2&limit=10")

        assert response.status_code == 200
        assert response.json()["page"] == 2

    @patch("presentation.views.user_views.UserManagementService")
    @patch("presentation.views.user_views.AuditLogger")
    def test_view_user_success(self, mock_audit, mock_service_class):
        mock_service = Mock()
        mock_service.get_user_by_id.return_value = {
            "user_id": "user-123",
            "email": "user@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "bio": "",
            "profile_picture_url": None,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
        }
        mock_service_class.return_value = mock_service

        client = Client()
        response = client.get("/api/superadmin/users/user-123/")

        assert response.status_code == 200
        assert response.json()["user_id"] == "user-123"

    @patch("presentation.views.user_views.UserManagementService")
    @patch("presentation.views.user_views.AuditLogger")
    def test_deactivate_user_success(self, mock_audit, mock_service_class):
        mock_service = Mock()
        mock_service.get_user_by_id.return_value = {"id": "user-123", "is_active": True}
        mock_service.deactivate_user.return_value = {
            "id": "user-123",
            "is_active": False,
            "message": "User deactivated",
        }
        mock_service_class.return_value = mock_service

        client = Client()
        response = client.post("/api/superadmin/users/user-123/deactivate/")

        assert response.status_code == 200
        assert response.json()["is_active"] is False
