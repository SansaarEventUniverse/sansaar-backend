import pytest
from domain.models import AuditTrail, ComplianceReport
from application.services.audit_trail_service import AuditTrailService
from application.services.compliance_service import ComplianceService
from application.services.audit_reporting_service import AuditReportingService


@pytest.mark.django_db
class TestAuditTrailService:
    def test_log_action(self):
        service = AuditTrailService()
        audit = service.log_action("user-123", "login", "auth")
        assert audit.action == "login"

    def test_get_user_audit_trail(self):
        AuditTrail.objects.create(user_id="user-123", action="login", resource="auth")
        service = AuditTrailService()
        trails = service.get_user_audit_trail("user-123")
        assert len(trails) == 1


@pytest.mark.django_db
class TestComplianceService:
    def test_create_compliance_report(self):
        service = ComplianceService()
        report = service.create_compliance_report("gdpr", "compliant", {"issues": 0})
        assert report.report_type == "gdpr"

    def test_check_compliance(self):
        ComplianceReport.objects.create(report_type="hipaa", status="compliant")
        service = ComplianceService()
        is_compliant = service.check_compliance("hipaa")
        assert is_compliant is True


@pytest.mark.django_db
class TestAuditReportingService:
    def test_generate_audit_report(self):
        AuditTrail.objects.create(user_id="user-123", action="login", resource="auth")
        service = AuditReportingService()
        report = service.generate_audit_report("user-123")
        assert "total_actions" in report

    def test_search_audit_trail(self):
        AuditTrail.objects.create(user_id="user-123", action="login", resource="auth")
        service = AuditReportingService()
        results = service.search_audit_trail({"action": "login"})
        assert len(results) == 1
