import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from application.ticket_type_service import (
    CreateTicketTypeService,
    UpdateTicketTypeService,
)
from infrastructure.repositories.ticket_type_repository import TicketTypeRepository
from presentation.serializers.ticket_type_serializers import (
    TicketTypeSerializer,
    CreateTicketTypeSerializer,
    UpdateTicketTypeSerializer,
)


@api_view(['POST'])
def create_ticket_type(request, event_id):
    """Create a ticket type for an event."""
    try:
        event_uuid = uuid.UUID(event_id)
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Add event_id to request data
    data = request.data.copy()
    data['event_id'] = str(event_uuid)
    
    serializer = CreateTicketTypeSerializer(data=data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        validated_data = serializer.validated_data
        validated_data['event_id'] = event_uuid
        service = CreateTicketTypeService()
        ticket_type = service.execute(validated_data)
        return Response(
            TicketTypeSerializer(ticket_type).data,
            status=status.HTTP_201_CREATED
        )
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_ticket_type(request, ticket_type_id):
    """Update a ticket type."""
    try:
        ticket_uuid = uuid.UUID(ticket_type_id)
    except ValueError:
        return Response({'error': 'Invalid ticket type ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = UpdateTicketTypeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = UpdateTicketTypeService()
        ticket_type = service.execute(ticket_uuid, serializer.validated_data)
        return Response(TicketTypeSerializer(ticket_type).data)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_ticket_types(request, event_id):
    """Get all ticket types for an event."""
    try:
        event_uuid = uuid.UUID(event_id)
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    repository = TicketTypeRepository()
    active_only = request.query_params.get('active_only', 'true').lower() == 'true'
    ticket_types = repository.get_by_event(event_uuid, active_only=active_only)
    
    return Response(TicketTypeSerializer(ticket_types, many=True).data)
