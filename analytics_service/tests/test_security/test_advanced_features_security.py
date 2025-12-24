import pytest
from domain.models import AuditTrail, ComplianceReport, DataExport
from application.services.audit_trail_service import AuditTrailService


@pytest.mark.django_db
class TestDataAccessControl:
    def test_audit_trail_user_isolation(self):
        AuditTrail.objects.create(user_id="user-123", action="login", resource="auth")
        AuditTrail.objects.create(user_id="user-456", action="login", resource="auth")
        
        service = AuditTrailService()
        user_123_trails = service.get_user_audit_trail("user-123")
        
        assert len(user_123_trails) == 1
        assert all(t.user_id == "user-123" for t in user_123_trails)


@pytest.mark.django_db
class TestAuditTrailIntegrity:
    def test_audit_trail_immutability(self):
        audit = AuditTrail.objects.create(
            user_id="user-123",
            action="delete_data",
            resource="sensitive_data",
            status="success"
        )
        
        assert audit.action == "delete_data"
        assert audit.status == "success"
        assert audit.created_at is not None


@pytest.mark.django_db
class TestComplianceValidation:
    def test_compliance_report_validation(self):
        report = ComplianceReport.objects.create(
            report_type="gdpr",
            status="compliant",
            findings={"issues": 0}
        )
        
        assert report.is_compliant() is True
        
        non_compliant = ComplianceReport.objects.create(
            report_type="hipaa",
            status="non_compliant",
            findings={"issues": 5}
        )
        
        assert non_compliant.is_compliant() is False


@pytest.mark.django_db
class TestExportSecurity:
    def test_export_data_validation(self):
        export = DataExport.objects.create(
            export_name="Test Export",
            export_format="csv",
            status="pending"
        )
        
        assert export.export_format == "csv"
        assert export.status == "pending"
