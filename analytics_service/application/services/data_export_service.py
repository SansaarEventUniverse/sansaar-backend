from domain.models import DataExport


class DataExportService:
    def create_export(self, export_name: str, export_format: str):
        return DataExport.objects.create(
            export_name=export_name,
            export_format=export_format,
            status="pending"
        )

    def get_export_status(self, export_id: int):
        export = DataExport.objects.get(id=export_id)
        return export.status
