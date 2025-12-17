from domain.models import CustomReport


class ReportExporter:
    def export(self, report_id: int, format: str):
        report = CustomReport.objects.get(id=report_id)
        return {
            "name": report.name,
            "type": report.report_type,
            "config": report.config
        }
