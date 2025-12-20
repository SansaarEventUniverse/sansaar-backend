import pytest
from django.core.exceptions import ValidationError
from domain.models import DataExport, ExportTemplate


@pytest.mark.django_db
class TestDataExport:
    def test_create_data_export(self):
        export = DataExport.objects.create(
            export_name="Sales Export",
            export_format="csv",
            status="pending"
        )
        assert export.export_name == "Sales Export"
        assert export.export_format == "csv"

    def test_export_name_required(self):
        with pytest.raises(ValidationError):
            export = DataExport(export_format="csv")
            export.full_clean()

    def test_is_completed(self):
        export = DataExport.objects.create(
            export_name="Test",
            export_format="json",
            status="completed"
        )
        assert export.is_completed() is True


@pytest.mark.django_db
class TestExportTemplate:
    def test_create_export_template(self):
        template = ExportTemplate.objects.create(
            template_name="Monthly Report",
            export_format="pdf",
            config={"columns": ["date", "revenue"]}
        )
        assert template.template_name == "Monthly Report"
        assert template.export_format == "pdf"

    def test_template_name_required(self):
        with pytest.raises(ValidationError):
            template = ExportTemplate(export_format="csv")
            template.full_clean()

    def test_is_active_default(self):
        template = ExportTemplate.objects.create(
            template_name="Test",
            export_format="excel"
        )
        assert template.is_active is True
