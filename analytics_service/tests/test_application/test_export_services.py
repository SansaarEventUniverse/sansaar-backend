import pytest
from domain.models import DataExport, ExportTemplate
from application.services.data_export_service import DataExportService
from application.services.export_template_service import ExportTemplateService
from application.services.integration_service import IntegrationService


@pytest.mark.django_db
class TestDataExportService:
    def test_create_export(self):
        service = DataExportService()
        export = service.create_export("Sales Data", "csv")
        assert export.export_name == "Sales Data"

    def test_get_export_status(self):
        export = DataExport.objects.create(export_name="Test", export_format="json", status="completed")
        service = DataExportService()
        status = service.get_export_status(export.id)
        assert status == "completed"


@pytest.mark.django_db
class TestExportTemplateService:
    def test_create_template(self):
        service = ExportTemplateService()
        template = service.create_template("Monthly", "pdf", {"columns": ["date"]})
        assert template.template_name == "Monthly"

    def test_get_active_templates(self):
        ExportTemplate.objects.create(template_name="T1", export_format="csv", is_active=True)
        ExportTemplate.objects.create(template_name="T2", export_format="pdf", is_active=False)
        service = ExportTemplateService()
        templates = service.get_active_templates()
        assert len(templates) == 1


@pytest.mark.django_db
class TestIntegrationService:
    def test_export_data(self):
        service = IntegrationService()
        result = service.export_data({"data": [1, 2, 3]}, "json")
        assert "exported" in result

    def test_schedule_export(self):
        service = IntegrationService()
        export = service.schedule_export("Weekly Report", "csv", "weekly")
        assert export.export_name == "Weekly Report"
