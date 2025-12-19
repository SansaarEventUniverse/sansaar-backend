import pytest
from domain.models import CustomReport, ReportTemplate
from infrastructure.generation.report_generator import ReportGenerator
from infrastructure.processing.template_processor import TemplateProcessor
from infrastructure.cache.report_cache import ReportCache
from infrastructure.export.report_exporter import ReportExporter


@pytest.mark.django_db
class TestReportGenerator:
    def test_generate(self):
        report = CustomReport.objects.create(
            name="Test",
            report_type="sales",
            config={"metrics": ["revenue"]}
        )
        generator = ReportGenerator()
        result = generator.generate(report.id)
        assert "report_id" in result


@pytest.mark.django_db
class TestTemplateProcessor:
    def test_process_template(self):
        template = ReportTemplate.objects.create(
            name="Template",
            template_type="monthly",
            template_config={"period": "month"}
        )
        processor = TemplateProcessor()
        result = processor.process(template.id)
        assert isinstance(result, dict)


@pytest.mark.django_db
class TestReportCache:
    def test_cache_report(self):
        cache = ReportCache()
        cache.set(1, {"data": "test"})
        result = cache.get(1)
        assert result["data"] == "test"


@pytest.mark.django_db
class TestReportExporter:
    def test_export_report(self):
        report = CustomReport.objects.create(
            name="Test",
            report_type="sales",
            config={"metrics": ["revenue"]}
        )
        exporter = ReportExporter()
        result = exporter.export(report.id, "json")
        assert "name" in result
