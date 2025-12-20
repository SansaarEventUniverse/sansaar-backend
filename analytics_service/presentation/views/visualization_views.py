from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from application.services.visualization_service import VisualizationService
from application.services.chart_generation_service import ChartGenerationService
from infrastructure.export.chart_exporter import ChartExporter
from presentation.serializers.visualization_serializers import (
    VisualizationSerializer, ChartSerializer, ChartCreateSerializer
)


class GetVisualizationView(APIView):
    def get(self, request, visualization_id):
        try:
            service = VisualizationService()
            viz = service.get_visualization(visualization_id)
            serializer = VisualizationSerializer(viz)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)


class CreateVisualizationView(APIView):
    def post(self, request):
        service = VisualizationService()
        viz = service.create_visualization(
            request.data['name'],
            request.data['visualization_type'],
            request.data.get('config', {})
        )
        serializer = VisualizationSerializer(viz)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateChartView(APIView):
    def post(self, request):
        serializer = ChartCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            service = ChartGenerationService()
            chart = service.generate_chart(
                serializer.validated_data['visualization_id'],
                serializer.validated_data['chart_type'],
                serializer.validated_data['data'],
                serializer.validated_data.get('config', {})
            )
            
            response_serializer = ChartSerializer(chart)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ExportChartView(APIView):
    def get(self, request, chart_id):
        exporter = ChartExporter()
        data = exporter.export(chart_id, 'json')
        return Response(data)
