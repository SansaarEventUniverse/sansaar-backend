from domain.models import CustomReport


class ReportBuilderService:
    def build_report(self, name: str, report_type: str, config: dict = None):
        return CustomReport.objects.create(
            name=name,
            report_type=report_type,
            config=config or {}
        )

    def get_report(self, report_id: int):
        return CustomReport.objects.get(id=report_id)
