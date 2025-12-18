from domain.models import ReportTemplate


class TemplateManagementService:
    def create_template(self, name: str, template_type: str, template_config: dict = None):
        return ReportTemplate.objects.create(
            name=name,
            template_type=template_type,
            template_config=template_config or {}
        )

    def get_active_templates(self):
        return list(ReportTemplate.objects.filter(is_active=True))
