import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from application.clone_service import (
    CloneEventService,
    BulkCloneService,
)
from presentation.serializers.clone_serializers import (
    CloneEventSerializer,
    BulkCloneSerializer,
    CloneSeriesSerializer,
    EventCloneInfoSerializer,
)
from presentation.serializers.event_serializers import EventSerializer


@api_view(['POST'])
def clone_event(request, event_id):
    """Clone an event."""
    try:
        event_uuid = uuid.UUID(event_id)
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = CloneEventSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = CloneEventService()
        cloned = service.clone_event(
            event_uuid,
            serializer.validated_data['cloned_by'],
            serializer.validated_data.get('customizations'),
            serializer.validated_data.get('reason', '')
        )
        
        return Response(
            EventSerializer(cloned).data,
            status=status.HTTP_201_CREATED
        )
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def bulk_clone(request):
    """Bulk clone events."""
    serializer = BulkCloneSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    service = BulkCloneService()
    cloned = service.bulk_clone(
        serializer.validated_data['event_ids'],
        serializer.validated_data['cloned_by'],
        serializer.validated_data.get('customizations')
    )
    
    return Response(
        EventSerializer(cloned, many=True).data,
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
def clone_series(request, event_id):
    """Clone event as a series."""
    try:
        event_uuid = uuid.UUID(event_id)
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = CloneSeriesSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = BulkCloneService()
        series = service.clone_series(
            event_uuid,
            serializer.validated_data['cloned_by'],
            serializer.validated_data['count'],
            serializer.validated_data.get('interval_days', 7)
        )
        
        return Response(
            EventSerializer(series, many=True).data,
            status=status.HTTP_201_CREATED
        )
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_clones(request, event_id):
    """Get all clones of an event."""
    try:
        event_uuid = uuid.UUID(event_id)
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    service = CloneEventService()
    clones = service.get_clones(event_uuid)
    
    return Response(EventSerializer(clones, many=True).data)


@api_view(['GET'])
def get_clone_info(request, event_id):
    """Get clone information for an event."""
    try:
        event_uuid = uuid.UUID(event_id)
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    from domain.clone import EventClone
    try:
        clone_record = EventClone.objects.get(cloned_event_id=event_uuid)
        return Response(EventCloneInfoSerializer(clone_record).data)
    except EventClone.DoesNotExist:
        return Response({'error': 'Not a cloned event'}, status=status.HTTP_404_NOT_FOUND)
