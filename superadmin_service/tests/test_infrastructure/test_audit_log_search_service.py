import pytest

from infrastructure.services.audit_log_search_service import AuditLogSearchService


@pytest.mark.django_db
def test_search_all_logs():
    service = AuditLogSearchService()
    result = service.search(page=1, limit=50)

    assert "logs" in result
    assert "total" in result


@pytest.mark.django_db
def test_search_with_event_type():
    service = AuditLogSearchService()
    result = service.search(event_type="SUPERADMIN_LOGIN", page=1, limit=10)

    assert result["page"] == 1
    assert result["limit"] == 10


@pytest.mark.django_db
def test_search_with_date_range():
    service = AuditLogSearchService()
    result = service.search(start_date="2026-01-01", end_date="2026-12-31", page=1, limit=10)

    assert "logs" in result
