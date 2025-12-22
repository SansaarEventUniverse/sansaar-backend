import pytest
from django.core.exceptions import ValidationError
from domain.models import AuditTrail, ComplianceReport


@pytest.mark.django_db
class TestAuditTrail:
    def test_create_audit_trail(self):
        audit = AuditTrail.objects.create(
            user_id="user-123",
            action="login",
            resource="auth",
            status="success"
        )
        assert audit.user_id == "user-123"
        assert audit.action == "login"

    def test_action_required(self):
        with pytest.raises(ValidationError):
            audit = AuditTrail(user_id="user-123")
            audit.full_clean()

    def test_is_successful(self):
        audit = AuditTrail.objects.create(
            user_id="user-123",
            action="update",
            resource="profile",
            status="success"
        )
        assert audit.is_successful() is True


@pytest.mark.django_db
class TestComplianceReport:
    def test_create_compliance_report(self):
        report = ComplianceReport.objects.create(
            report_type="gdpr",
            status="compliant",
            findings={"issues": 0}
        )
        assert report.report_type == "gdpr"
        assert report.status == "compliant"

    def test_report_type_required(self):
        with pytest.raises(ValidationError):
            report = ComplianceReport(status="compliant")
            report.full_clean()

    def test_is_compliant(self):
        report = ComplianceReport.objects.create(
            report_type="hipaa",
            status="compliant"
        )
        assert report.is_compliant() is True
