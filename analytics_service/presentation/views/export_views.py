from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from application.services.data_export_service import DataExportService
from application.services.integration_service import IntegrationService
from infrastructure.export.export_pipeline import ExportPipeline
from presentation.serializers.export_serializers import (
    DataExportSerializer, ExportDataSerializer, ScheduleExportSerializer
)


class ExportDataView(APIView):
    def post(self, request):
        serializer = ExportDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        service = DataExportService()
        export = service.create_export(
            serializer.validated_data['export_name'],
            serializer.validated_data['export_format']
        )
        
        # Process export
        pipeline = ExportPipeline()
        pipeline.process(export.id, serializer.validated_data['data'])
        
        response_serializer = DataExportSerializer(export)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class ScheduleExportView(APIView):
    def post(self, request):
        serializer = ScheduleExportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        service = IntegrationService()
        export = service.schedule_export(
            serializer.validated_data['export_name'],
            serializer.validated_data['export_format'],
            serializer.validated_data['schedule']
        )
        
        response_serializer = DataExportSerializer(export)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class GetExportStatusView(APIView):
    def get(self, request, export_id):
        try:
            service = DataExportService()
            export_status = service.get_export_status(export_id)
            return Response({'status': export_status})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
