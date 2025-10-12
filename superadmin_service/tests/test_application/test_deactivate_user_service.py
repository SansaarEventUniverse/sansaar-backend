from unittest.mock import Mock

import pytest
from django.core.exceptions import ValidationError

from application.deactivate_user_service import DeactivateUserService


class TestDeactivateUserService:
    def test_deactivate_user_success(self):
        user_mgmt_service = Mock()
        user_mgmt_service.get_user_by_id.return_value = {"id": "user-123", "is_active": True}
        user_mgmt_service.deactivate_user.return_value = {"id": "user-123", "is_active": False}

        audit_logger = Mock()
        service = DeactivateUserService(user_mgmt_service, audit_logger)

        result = service.deactivate_user("user-123", "admin-123", "admin@example.com")

        assert result["is_active"] is False
        user_mgmt_service.deactivate_user.assert_called_once_with("user-123")
        audit_logger.log_event.assert_called_once()

    def test_deactivate_already_inactive_user(self):
        user_mgmt_service = Mock()
        user_mgmt_service.get_user_by_id.return_value = {"id": "user-123", "is_active": False}

        service = DeactivateUserService(user_mgmt_service)

        with pytest.raises(ValidationError, match="User is already deactivated"):
            service.deactivate_user("user-123", "admin-123", "admin@example.com")

    def test_deactivate_user_without_audit(self):
        user_mgmt_service = Mock()
        user_mgmt_service.get_user_by_id.return_value = {"id": "user-123", "is_active": True}
        user_mgmt_service.deactivate_user.return_value = {"id": "user-123", "is_active": False}

        service = DeactivateUserService(user_mgmt_service)
        result = service.deactivate_user("user-123", "admin-123", "admin@example.com")

        assert result["is_active"] is False
