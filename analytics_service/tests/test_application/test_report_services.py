import pytest
from domain.models import CustomReport, ReportTemplate
from application.services.report_builder_service import ReportBuilderService
from application.services.template_management_service import TemplateManagementService
from application.services.report_generation_service import ReportGenerationService


@pytest.mark.django_db
class TestReportBuilderService:
    def test_build_report(self):
        service = ReportBuilderService()
        report = service.build_report("Sales Report", "sales", {"metrics": ["revenue"]})
        assert report.name == "Sales Report"

    def test_get_report(self):
        report = CustomReport.objects.create(name="Test", report_type="analytics")
        service = ReportBuilderService()
        result = service.get_report(report.id)
        assert result.id == report.id


@pytest.mark.django_db
class TestTemplateManagementService:
    def test_create_template(self):
        service = TemplateManagementService()
        template = service.create_template("Monthly", "monthly", {"period": "month"})
        assert template.name == "Monthly"

    def test_get_active_templates(self):
        ReportTemplate.objects.create(name="T1", template_type="daily", is_active=True)
        ReportTemplate.objects.create(name="T2", template_type="weekly", is_active=False)
        service = TemplateManagementService()
        templates = service.get_active_templates()
        assert len(templates) == 1


@pytest.mark.django_db
class TestReportGenerationService:
    def test_generate_report(self):
        report = CustomReport.objects.create(
            name="Test Report",
            report_type="sales",
            config={"metrics": ["revenue"]}
        )
        service = ReportGenerationService()
        result = service.generate_report(report.id)
        assert "report_id" in result

    def test_generate_from_template(self):
        template = ReportTemplate.objects.create(
            name="Template",
            template_type="monthly",
            template_config={"period": "month"}
        )
        service = ReportGenerationService()
        result = service.generate_from_template(template.id, "Generated Report")
        assert result.name == "Generated Report"
