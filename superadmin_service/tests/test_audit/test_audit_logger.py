from unittest.mock import Mock, patch

from infrastructure.audit.audit_logger import AuditLogger


class TestAuditLogger:
    @patch("infrastructure.audit.audit_logger.Elasticsearch")
    def test_log_superadmin_login(self, mock_es):
        mock_es_instance = Mock()
        mock_es.return_value = mock_es_instance

        logger = AuditLogger()
        logger.log_superadmin_login("admin-123", "admin@example.com", "192.168.1.1")

        mock_es_instance.index.assert_called_once()
        call_args = mock_es_instance.index.call_args
        assert call_args[1]["index"] == "superadmin_audit_logs"
        assert call_args[1]["document"]["event_type"] == "SUPERADMIN_LOGIN"
        assert call_args[1]["document"]["admin_id"] == "admin-123"

    @patch("infrastructure.audit.audit_logger.Elasticsearch")
    def test_log_superadmin_logout(self, mock_es):
        mock_es_instance = Mock()
        mock_es.return_value = mock_es_instance

        logger = AuditLogger()
        logger.log_superadmin_logout("admin-123", "admin@example.com", "192.168.1.1")

        mock_es_instance.index.assert_called_once()
        call_args = mock_es_instance.index.call_args
        assert call_args[1]["document"]["event_type"] == "SUPERADMIN_LOGOUT"

    @patch("infrastructure.audit.audit_logger.Elasticsearch")
    def test_log_superadmin_login_failed(self, mock_es):
        mock_es_instance = Mock()
        mock_es.return_value = mock_es_instance

        logger = AuditLogger()
        logger.log_superadmin_login_failed("admin@example.com", "192.168.1.1", "Invalid password")

        mock_es_instance.index.assert_called_once()
        call_args = mock_es_instance.index.call_args
        assert call_args[1]["document"]["event_type"] == "SUPERADMIN_LOGIN_FAILED"
        assert call_args[1]["document"]["metadata"]["reason"] == "Invalid password"

    @patch("infrastructure.audit.audit_logger.Elasticsearch")
    def test_log_ip_whitelist_violation(self, mock_es):
        mock_es_instance = Mock()
        mock_es.return_value = mock_es_instance

        logger = AuditLogger()
        logger.log_ip_whitelist_violation("admin@example.com", "192.168.1.1")

        mock_es_instance.index.assert_called_once()
        call_args = mock_es_instance.index.call_args
        assert call_args[1]["document"]["event_type"] == "IP_WHITELIST_VIOLATION"
