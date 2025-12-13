from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from application.services.event_analytics_service import EventAnalyticsService
from application.services.attendance_tracking_service import AttendanceTrackingService
from application.services.metrics_reporting_service import MetricsReportingService
from presentation.serializers.event_analytics_serializers import (
    EventMetricsSerializer, AttendanceAnalyticsSerializer, CheckInSerializer, CheckOutSerializer
)


class TrackViewAPI(APIView):
    def post(self, request, event_id):
        service = EventAnalyticsService()
        metrics = service.track_event_view(event_id)
        return Response(EventMetricsSerializer(metrics).data)


class TrackRegistrationAPI(APIView):
    def post(self, request, event_id):
        service = EventAnalyticsService()
        metrics = service.track_event_registration(event_id)
        return Response(EventMetricsSerializer(metrics).data)


class EventMetricsAPI(APIView):
    def get(self, request, event_id):
        service = MetricsReportingService()
        metrics = service.get_event_metrics(event_id)
        return Response(metrics)


class CheckInAPI(APIView):
    def post(self, request, event_id):
        serializer = CheckInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        service = AttendanceTrackingService()
        attendance = service.check_in_user(event_id, serializer.validated_data['user_id'])
        return Response(AttendanceAnalyticsSerializer(attendance).data)


class CheckOutAPI(APIView):
    def post(self, request, event_id):
        serializer = CheckOutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        service = AttendanceTrackingService()
        attendance = service.check_out_user(event_id, serializer.validated_data['user_id'])
        return Response(AttendanceAnalyticsSerializer(attendance).data)


class MetricsExportAPI(APIView):
    def get(self, request, event_id):
        service = MetricsReportingService()
        metrics = service.get_event_metrics(event_id)
        return Response(metrics)


class MetricsExportCSVAPI(APIView):
    def get(self, request, event_id):
        service = MetricsReportingService()
        data = service.export_metrics(event_id, 'csv')
        response = HttpResponse(data, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="metrics_{event_id}.csv"'
        return response
