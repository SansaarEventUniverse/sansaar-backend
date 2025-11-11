import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from application.calendar_service import CalendarEventManagementService
from infrastructure.services.calendar_integration_service import CalendarWebhookHandler
from presentation.serializers.calendar_serializers import (
    CalendarEventSerializer,
    SyncCalendarSerializer,
    CalendarWebhookSerializer,
)


@api_view(['GET'])
def export_to_calendar(request, event_id):
    """Export event to iCal format."""
    try:
        event_uuid = uuid.UUID(event_id)
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = CalendarEventManagementService()
        ical_content = service.export_to_ical(event_uuid)
        
        response = HttpResponse(ical_content, content_type='text/calendar')
        response['Content-Disposition'] = f'attachment; filename="event-{event_id}.ics"'
        return response
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def sync_calendar(request, event_id):
    """Sync event to external calendar."""
    try:
        event_uuid = uuid.UUID(event_id)
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = SyncCalendarSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = CalendarEventManagementService()
        cal_event = service.sync_to_calendar(
            event_uuid,
            serializer.validated_data['user_id'],
            serializer.validated_data['provider']
        )
        
        return Response(
            CalendarEventSerializer(cal_event).data,
            status=status.HTTP_201_CREATED
        )
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def calendar_webhook(request):
    """Handle calendar webhook."""
    serializer = CalendarWebhookSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    handler = CalendarWebhookHandler()
    
    if serializer.validated_data['provider'] == 'google':
        result = handler.handle_google_webhook(serializer.validated_data)
        return Response(result, status=status.HTTP_200_OK)
    
    return Response({'error': 'Unsupported provider'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_calendar_syncs(request, event_id):
    """Get calendar syncs for event."""
    try:
        event_uuid = uuid.UUID(event_id)
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    from domain.calendar import CalendarEvent
    syncs = CalendarEvent.objects.filter(event_id=event_uuid)
    
    return Response(CalendarEventSerializer(syncs, many=True).data)
