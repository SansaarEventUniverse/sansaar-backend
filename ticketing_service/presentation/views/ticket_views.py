import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from application.ticket_service import (
    ValidateQRCodeService,
    TicketCheckInService,
)
from domain.ticket import Ticket
from presentation.serializers.ticket_serializers import (
    TicketSerializer,
    ValidateQRCodeSerializer,
    CheckInSerializer,
)


@api_view(['POST'])
def validate_qr_code(request):
    """Validate a QR code."""
    serializer = ValidateQRCodeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = ValidateQRCodeService()
        result = service.execute(serializer.validated_data['qr_code_data'])
        return Response(result)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def check_in_ticket(request, ticket_id):
    """Check in a ticket."""
    try:
        ticket_uuid = uuid.UUID(ticket_id)
    except ValueError:
        return Response({'error': 'Invalid ticket ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = CheckInSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = TicketCheckInService()
        ticket = service.execute(ticket_uuid, serializer.validated_data['checked_in_by'])
        return Response(TicketSerializer(ticket).data)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_ticket(request, ticket_id):
    """Get ticket details."""
    try:
        ticket_uuid = uuid.UUID(ticket_id)
    except ValueError:
        return Response({'error': 'Invalid ticket ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        ticket = Ticket.objects.get(id=ticket_uuid)
        return Response(TicketSerializer(ticket).data)
    except Ticket.DoesNotExist:
        return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
