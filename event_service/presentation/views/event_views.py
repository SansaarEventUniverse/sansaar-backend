import uuid
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from application.event_service import (
    CreateEventService,
    UpdateEventService,
    GetEventService,
    SaveEventDraftService,
    GetEventDraftService,
)
from presentation.serializers.event_serializers import EventSerializer, EventDraftSerializer


@api_view(['POST'])
def create_event(request):
    """Create a new event."""
    serializer = EventSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = CreateEventService()
        event = service.execute(serializer.validated_data)
        return Response(
            EventSerializer(event).data,
            status=status.HTTP_201_CREATED
        )
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_event(request, event_id):
    """Get event by ID."""
    try:
        service = GetEventService()
        event = service.execute(uuid.UUID(event_id))
        return Response(EventSerializer(event).data)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
def update_event(request, event_id):
    """Update an event."""
    try:
        service = UpdateEventService()
        event = service.execute(uuid.UUID(event_id), request.data)
        return Response(EventSerializer(event).data)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def save_draft(request):
    """Save event draft."""
    serializer = EventDraftSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = SaveEventDraftService()
        draft = service.execute(
            organizer_id=serializer.validated_data['organizer_id'],
            draft_data=serializer.validated_data['draft_data'],
            event_id=serializer.validated_data.get('event_id')
        )
        return Response(
            EventDraftSerializer(draft).data,
            status=status.HTTP_201_CREATED
        )
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_draft(request):
    """Get event draft."""
    organizer_id = request.query_params.get('organizer_id')
    event_id = request.query_params.get('event_id')
    
    if not organizer_id:
        return Response(
            {'error': 'organizer_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        service = GetEventDraftService()
        draft = service.execute(
            organizer_id=uuid.UUID(organizer_id),
            event_id=uuid.UUID(event_id) if event_id else None
        )
        if draft:
            return Response(EventDraftSerializer(draft).data)
        return Response({'error': 'Draft not found'}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({'error': 'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)
