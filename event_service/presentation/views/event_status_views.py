import uuid
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from application.event_status_service import (
    PublishEventService,
    UnpublishEventService,
    CancelEventService,
    CompleteEventService,
)
from presentation.serializers.event_serializers import EventSerializer


@api_view(['POST'])
def publish_event(request, event_id):
    """Publish an event."""
    try:
        service = PublishEventService()
        event = service.execute(uuid.UUID(event_id))
        return Response(EventSerializer(event).data)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def unpublish_event(request, event_id):
    """Unpublish an event."""
    try:
        service = UnpublishEventService()
        event = service.execute(uuid.UUID(event_id))
        return Response(EventSerializer(event).data)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def cancel_event(request, event_id):
    """Cancel an event."""
    try:
        service = CancelEventService()
        event = service.execute(uuid.UUID(event_id))
        return Response(EventSerializer(event).data)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def complete_event(request, event_id):
    """Complete an event."""
    try:
        service = CompleteEventService()
        event = service.execute(uuid.UUID(event_id))
        return Response(EventSerializer(event).data)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)
