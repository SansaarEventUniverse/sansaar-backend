from unittest.mock import Mock

from application.list_all_users_service import ListAllUsersService


class TestListAllUsersService:
    def test_list_users_default_pagination(self):
        user_mgmt_service = Mock()
        user_mgmt_service.get_users.return_value = {
            "users": [{"id": "1", "email": "user1@example.com"}],
            "total": 1,
            "page": 1,
            "limit": 50,
        }

        service = ListAllUsersService(user_mgmt_service)
        result = service.list_users()

        assert result["total"] == 1
        assert len(result["users"]) == 1
        user_mgmt_service.get_users.assert_called_once_with(1, 50)

    def test_list_users_custom_pagination(self):
        user_mgmt_service = Mock()
        user_mgmt_service.get_users.return_value = {"users": [], "total": 0, "page": 2, "limit": 10}

        service = ListAllUsersService(user_mgmt_service)
        result = service.list_users(page=2, limit=10)

        assert result["page"] == 2
        assert result["limit"] == 10
        user_mgmt_service.get_users.assert_called_once_with(2, 10)
