from rest_framework.views import APIView
from rest_framework.response import Response
from application.services.performance_monitoring_service import PerformanceMonitoringService
from application.services.system_health_service import SystemHealthService
from application.services.alerting_service import AlertingService
from presentation.serializers.performance_serializers import PerformanceMetricSerializer, SystemHealthSerializer


class GetPerformanceView(APIView):
    def get(self, request):
        service = PerformanceMonitoringService()
        metrics = service.get_metrics()
        serializer = PerformanceMetricSerializer(metrics, many=True)
        return Response(serializer.data)


class SystemHealthView(APIView):
    def get(self, request):
        from domain.models import SystemHealth
        health_records = SystemHealth.objects.all()
        serializer = SystemHealthSerializer(health_records, many=True)
        return Response(serializer.data)


class AlertsView(APIView):
    def get(self, request):
        service = AlertingService()
        alerts = service.get_alerts()
        serializer = PerformanceMetricSerializer(alerts, many=True)
        return Response(serializer.data)
