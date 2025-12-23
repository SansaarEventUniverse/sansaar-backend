import pytest
from domain.models import AuditTrail, ComplianceReport
from infrastructure.audit.audit_logger import AuditLogger
from infrastructure.audit.compliance_monitor import ComplianceMonitor


@pytest.mark.django_db
class TestAuditLogger:
    def test_log_audit(self):
        logger = AuditLogger()
        audit = logger.log("user-123", "update", "profile")
        assert audit.action == "update"


@pytest.mark.django_db
class TestComplianceMonitor:
    def test_monitor_compliance(self):
        monitor = ComplianceMonitor()
        result = monitor.monitor("gdpr")
        assert "compliant" in result

    def test_generate_compliance_report(self):
        AuditTrail.objects.create(user_id="user-123", action="data_access", resource="user_data")
        monitor = ComplianceMonitor()
        report = monitor.generate_report("gdpr")
        assert report.report_type == "gdpr"
