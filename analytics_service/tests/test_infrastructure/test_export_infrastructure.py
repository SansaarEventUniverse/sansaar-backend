import pytest
from domain.models import DataExport
from infrastructure.export.export_pipeline import ExportPipeline
from infrastructure.export.format_converter import FormatConverter


@pytest.mark.django_db
class TestExportPipeline:
    def test_process_export(self):
        export = DataExport.objects.create(export_name="Test", export_format="csv")
        pipeline = ExportPipeline()
        result = pipeline.process(export.id, {"data": [1, 2, 3]})
        assert "status" in result


@pytest.mark.django_db
class TestFormatConverter:
    def test_convert_to_csv(self):
        converter = FormatConverter()
        result = converter.convert({"data": [1, 2, 3]}, "csv")
        assert isinstance(result, str)

    def test_convert_to_json(self):
        converter = FormatConverter()
        result = converter.convert({"data": [1, 2, 3]}, "json")
        assert isinstance(result, str)
