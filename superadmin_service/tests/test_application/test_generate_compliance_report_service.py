import pytest

from application.generate_compliance_report_service import GenerateComplianceReportService
from infrastructure.services.audit_log_search_service import AuditLogSearchService


@pytest.mark.django_db
def test_generate_report():
    search_service = AuditLogSearchService()
    service = GenerateComplianceReportService(search_service)

    csv_content = service.generate_report()

    assert "Timestamp" in csv_content
    assert "Event Type" in csv_content
    assert "Admin ID" in csv_content
