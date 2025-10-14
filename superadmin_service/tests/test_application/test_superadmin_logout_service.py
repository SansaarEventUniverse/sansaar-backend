from unittest.mock import Mock

from application.superadmin_logout_service import SuperAdminLogoutService


class TestSuperAdminLogoutService:
    def test_logout_success(self):
        jwt_service = Mock()
        service = SuperAdminLogoutService(jwt_service)

        result = service.logout("test_token")

        assert result["message"] == "Logged out successfully"
        jwt_service.blacklist_token.assert_called_once_with("test_token")
