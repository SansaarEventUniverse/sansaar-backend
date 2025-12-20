from domain.models import DataExport


class ExportPipeline:
    def process(self, export_id: int, data: dict):
        export = DataExport.objects.get(id=export_id)
        export.status = "processing"
        export.save()
        
        # Simulate processing
        export.status = "completed"
        export.save()
        
        return {"status": "completed", "export_id": export_id}
