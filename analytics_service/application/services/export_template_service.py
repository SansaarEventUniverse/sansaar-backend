from domain.models import ExportTemplate


class ExportTemplateService:
    def create_template(self, template_name: str, export_format: str, config: dict = None):
        return ExportTemplate.objects.create(
            template_name=template_name,
            export_format=export_format,
            config=config or {}
        )

    def get_active_templates(self):
        return list(ExportTemplate.objects.filter(is_active=True))
