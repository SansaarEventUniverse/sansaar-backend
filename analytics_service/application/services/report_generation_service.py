from domain.models import CustomReport, ReportTemplate


class ReportGenerationService:
    def generate_report(self, report_id: int):
        report = CustomReport.objects.get(id=report_id)
        return {
            "report_id": report.id,
            "name": report.name,
            "type": report.report_type,
            "data": report.config
        }

    def generate_from_template(self, template_id: int, report_name: str):
        template = ReportTemplate.objects.get(id=template_id)
        return CustomReport.objects.create(
            name=report_name,
            report_type=template.template_type,
            config=template.template_config
        )
