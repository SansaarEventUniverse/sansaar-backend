import pytest

from application.search_audit_logs_service import SearchAuditLogsService
from infrastructure.services.audit_log_search_service import AuditLogSearchService


@pytest.mark.django_db
def test_search_audit_logs():
    search_service = AuditLogSearchService()
    service = SearchAuditLogsService(search_service)

    result = service.search_logs(page=1, limit=50)

    assert "logs" in result
    assert "total" in result
    assert "page" in result
    assert "limit" in result


@pytest.mark.django_db
def test_search_with_filters():
    search_service = AuditLogSearchService()
    service = SearchAuditLogsService(search_service)

    result = service.search_logs(event_type="SUPERADMIN_LOGIN", page=1, limit=10)

    assert result["page"] == 1
    assert result["limit"] == 10
