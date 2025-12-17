import pytest
from django.core.exceptions import ValidationError
from domain.models import CustomReport, ReportTemplate


@pytest.mark.django_db
class TestCustomReport:
    def test_create_custom_report(self):
        report = CustomReport.objects.create(
            name="Sales Report",
            report_type="sales",
            config={"metrics": ["revenue", "orders"]}
        )
        assert report.name == "Sales Report"
        assert report.report_type == "sales"

    def test_report_name_required(self):
        with pytest.raises(ValidationError):
            report = CustomReport(report_type="sales")
            report.full_clean()

    def test_get_metrics_count(self):
        report = CustomReport.objects.create(
            name="Test Report",
            report_type="analytics",
            config={"metrics": ["a", "b", "c"]}
        )
        assert report.get_metrics_count() == 3


@pytest.mark.django_db
class TestReportTemplate:
    def test_create_report_template(self):
        template = ReportTemplate.objects.create(
            name="Monthly Template",
            template_type="monthly",
            template_config={"period": "month"}
        )
        assert template.name == "Monthly Template"
        assert template.template_type == "monthly"

    def test_template_name_required(self):
        with pytest.raises(ValidationError):
            template = ReportTemplate(template_type="weekly")
            template.full_clean()

    def test_is_active_default(self):
        template = ReportTemplate.objects.create(
            name="Test Template",
            template_type="daily"
        )
        assert template.is_active is True
