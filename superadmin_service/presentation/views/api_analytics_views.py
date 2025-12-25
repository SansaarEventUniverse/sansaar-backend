from rest_framework.views import APIView
from rest_framework.response import Response
from domain.models import APIUsage, APIMetrics
from presentation.serializers.api_analytics_serializers import APIUsageSerializer, APIMetricsSerializer


class GetAPIAnalyticsView(APIView):
    def get(self, request):
        usage_data = APIUsage.objects.all().order_by('-timestamp')[:100]
        serializer = APIUsageSerializer(usage_data, many=True)
        return Response(serializer.data)


class APIUsageReportView(APIView):
    def get(self, request):
        usage_data = APIUsage.objects.all().order_by('-timestamp')
        serializer = APIUsageSerializer(usage_data, many=True)
        return Response(serializer.data)


class APIMonitoringView(APIView):
    def get(self, request):
        metrics = APIMetrics.objects.all().order_by('-created_at')
        serializer = APIMetricsSerializer(metrics, many=True)
        return Response(serializer.data)
