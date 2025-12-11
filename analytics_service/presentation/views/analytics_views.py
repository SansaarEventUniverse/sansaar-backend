from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from application.services.analytics_processing_service import AnalyticsProcessingService
from application.services.realtime_analytics_service import RealTimeAnalyticsService
from presentation.serializers.analytics_serializers import AnalyticsEventSerializer, AnalyticsQuerySerializer
from domain.models import AnalyticsEvent


@api_view(['GET'])
def get_analytics(request):
    total = AnalyticsEvent.objects.count()
    unprocessed = AnalyticsEvent.objects.filter(is_processed=False).count()
    return Response({
        'total_events': total,
        'processed_events': total - unprocessed,
        'unprocessed_events': unprocessed
    })


@api_view(['GET'])
def get_realtime_metrics(request):
    service = RealTimeAnalyticsService()
    metrics = service.get_realtime_metrics()
    return Response(metrics)


@api_view(['POST'])
def analytics_query(request):
    serializer = AnalyticsQuerySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    queryset = AnalyticsEvent.objects.all()
    if serializer.validated_data.get('event_type'):
        queryset = queryset.filter(event_type=serializer.validated_data['event_type'])
    if serializer.validated_data.get('user_id'):
        queryset = queryset.filter(user_id=serializer.validated_data['user_id'])
    
    events = AnalyticsEventSerializer(queryset, many=True)
    return Response({'events': events.data, 'count': queryset.count()})


@api_view(['POST'])
def create_analytics_event(request):
    serializer = AnalyticsEventSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    service = AnalyticsProcessingService()
    event = service.process_event(serializer.validated_data)
    return Response(AnalyticsEventSerializer(event).data, status=status.HTTP_201_CREATED)
