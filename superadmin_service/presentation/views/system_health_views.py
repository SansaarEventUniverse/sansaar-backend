from rest_framework.views import APIView
from rest_framework.response import Response
from domain.models import SystemHealth, HealthCheck
from presentation.serializers.system_health_serializers import SystemHealthSerializer, HealthCheckSerializer


class GetSystemHealthView(APIView):
    def get(self, request):
        health_data = SystemHealth.objects.all().order_by('-created_at')
        serializer = SystemHealthSerializer(health_data, many=True)
        return Response(serializer.data)


class HealthCheckView(APIView):
    def get(self, request):
        checks = HealthCheck.objects.all().order_by('-checked_at')
        serializer = HealthCheckSerializer(checks, many=True)
        return Response(serializer.data)


class MonitoringDashboardView(APIView):
    def get(self, request):
        health_data = SystemHealth.objects.all().order_by('-created_at')[:10]
        serializer = SystemHealthSerializer(health_data, many=True)
        return Response(serializer.data)
