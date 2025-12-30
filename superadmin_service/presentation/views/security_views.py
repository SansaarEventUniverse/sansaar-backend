from rest_framework.views import APIView
from rest_framework.response import Response
from domain.models import SecurityEvent
from presentation.serializers.security_serializers import SecurityEventSerializer


class GetSecurityEventsView(APIView):
    def get(self, request):
        events = SecurityEvent.objects.all().order_by('-created_at')
        serializer = SecurityEventSerializer(events, many=True)
        return Response(serializer.data)


class SecurityDashboardView(APIView):
    def get(self, request):
        critical_events = SecurityEvent.objects.filter(severity__in=["high", "critical"]).count()
        total_events = SecurityEvent.objects.count()
        return Response({
            "total_events": total_events,
            "critical_events": critical_events
        })


class ThreatAnalysisView(APIView):
    def get(self, request):
        threats = SecurityEvent.objects.filter(severity__in=["high", "critical"])
        serializer = SecurityEventSerializer(threats, many=True)
        return Response(serializer.data)
