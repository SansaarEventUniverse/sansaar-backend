from domain.models import ReportTemplate


class TemplateProcessor:
    def process(self, template_id: int):
        template = ReportTemplate.objects.get(id=template_id)
        return {
            "template_id": template.id,
            "name": template.name,
            "config": template.template_config
        }
