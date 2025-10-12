from unittest.mock import Mock, patch
from infrastructure.audit.audit_logger import AuditLogger


class TestUserManagementAudit:
    @patch("infrastructure.audit.audit_logger.Elasticsearch")
    def test_log_user_viewed(self, mock_es):
        mock_es_instance = Mock()
        mock_es.return_value = mock_es_instance

        logger = AuditLogger()
        logger.log_event("SUPERADMIN_USER_VIEWED", "admin-123", "admin@example.com", "", {"viewed_user_id": "user-123"})

        mock_es_instance.index.assert_called_once()
        call_args = mock_es_instance.index.call_args
        assert call_args[1]["document"]["event_type"] == "SUPERADMIN_USER_VIEWED"

    @patch("infrastructure.audit.audit_logger.Elasticsearch")
    def test_log_user_deactivated(self, mock_es):
        mock_es_instance = Mock()
        mock_es.return_value = mock_es_instance

        logger = AuditLogger()
        logger.log_event(
            "SUPERADMIN_USER_DEACTIVATED", "admin-123", "admin@example.com", "", {"deactivated_user_id": "user-123"}
        )

        mock_es_instance.index.assert_called_once()
        call_args = mock_es_instance.index.call_args
        assert call_args[1]["document"]["event_type"] == "SUPERADMIN_USER_DEACTIVATED"
