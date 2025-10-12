from unittest.mock import Mock

from application.view_user_details_service import ViewUserDetailsService


class TestViewUserDetailsService:
    def test_get_user_success(self):
        user_mgmt_service = Mock()
        user_mgmt_service.get_user_by_id.return_value = {"id": "user-123", "email": "user@example.com"}

        audit_logger = Mock()
        service = ViewUserDetailsService(user_mgmt_service, audit_logger)

        result = service.get_user("user-123", "admin-123", "admin@example.com")

        assert result["id"] == "user-123"
        user_mgmt_service.get_user_by_id.assert_called_once_with("user-123")
        audit_logger.log_event.assert_called_once()

    def test_get_user_without_audit(self):
        user_mgmt_service = Mock()
        user_mgmt_service.get_user_by_id.return_value = {"id": "user-123", "email": "user@example.com"}

        service = ViewUserDetailsService(user_mgmt_service)
        result = service.get_user("user-123", "admin-123", "admin@example.com")

        assert result["id"] == "user-123"
