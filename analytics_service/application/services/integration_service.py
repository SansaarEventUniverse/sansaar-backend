from domain.models import DataExport


class IntegrationService:
    def export_data(self, data: dict, format: str):
        return {"exported": True, "format": format, "data": data}

    def schedule_export(self, export_name: str, export_format: str, schedule: str):
        return DataExport.objects.create(
            export_name=export_name,
            export_format=export_format,
            status="scheduled"
        )
