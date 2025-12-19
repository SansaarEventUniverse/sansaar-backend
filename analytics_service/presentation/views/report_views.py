from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from application.services.report_builder_service import ReportBuilderService
from application.services.template_management_service import TemplateManagementService
from application.services.report_generation_service import ReportGenerationService
from presentation.serializers.report_serializers import (
    CustomReportSerializer, ReportTemplateSerializer, BuildReportSerializer, GenerateReportSerializer
)


class BuildReportView(APIView):
    def post(self, request):
        serializer = BuildReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        service = ReportBuilderService()
        report = service.build_report(
            serializer.validated_data['name'],
            serializer.validated_data['report_type'],
            serializer.validated_data.get('config', {})
        )
        
        response_serializer = CustomReportSerializer(report)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class SaveTemplateView(APIView):
    def post(self, request):
        serializer = ReportTemplateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        service = TemplateManagementService()
        template = service.create_template(
            serializer.validated_data['name'],
            serializer.validated_data['template_type'],
            serializer.validated_data.get('template_config', {})
        )
        
        response_serializer = ReportTemplateSerializer(template)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        service = TemplateManagementService()
        templates = service.get_active_templates()
        serializer = ReportTemplateSerializer(templates, many=True)
        return Response(serializer.data)


class GenerateReportView(APIView):
    def post(self, request):
        serializer = GenerateReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            service = ReportGenerationService()
            result = service.generate_report(serializer.validated_data['report_id'])
            return Response(result)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
