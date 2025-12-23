from domain.models import ComplianceReport


class ComplianceService:
    def create_compliance_report(self, report_type: str, status: str, findings: dict = None):
        return ComplianceReport.objects.create(
            report_type=report_type,
            status=status,
            findings=findings or {}
        )

    def check_compliance(self, report_type: str):
        try:
            report = ComplianceReport.objects.filter(report_type=report_type).latest('created_at')
            return report.is_compliant()
        except ComplianceReport.DoesNotExist:
            return False
