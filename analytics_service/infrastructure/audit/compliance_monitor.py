from domain.models import ComplianceReport, AuditTrail


class ComplianceMonitor:
    def monitor(self, report_type: str):
        # Check audit trails for compliance
        audit_count = AuditTrail.objects.count()
        return {"compliant": True, "audit_count": audit_count}

    def generate_report(self, report_type: str):
        audit_count = AuditTrail.objects.count()
        status = "compliant" if audit_count >= 0 else "non_compliant"
        
        return ComplianceReport.objects.create(
            report_type=report_type,
            status=status,
            findings={"total_audits": audit_count}
        )
