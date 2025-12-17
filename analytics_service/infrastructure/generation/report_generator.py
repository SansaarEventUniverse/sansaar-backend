from domain.models import CustomReport


class ReportGenerator:
    def generate(self, report_id: int):
        report = CustomReport.objects.get(id=report_id)
        return {
            "report_id": report.id,
            "name": report.name,
            "type": report.report_type,
            "config": report.config
        }
