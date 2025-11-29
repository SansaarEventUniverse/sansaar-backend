from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from application.group_booking_service import (
    GroupBookingService,
    GroupPaymentService
)
from presentation.serializers.group_booking_serializers import (
    CreateGroupBookingSerializer,
    JoinGroupBookingSerializer,
    ProcessGroupPaymentSerializer,
    GroupBookingResponseSerializer
)


@api_view(['POST'])
def create_group_booking(request, event_id):
    """Create a new group booking."""
    data = request.data.copy()
    data['event_id'] = event_id
    
    serializer = CreateGroupBookingSerializer(data=data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = GroupBookingService()
        booking = service.create_booking(serializer.validated_data)
        
        response_data = {
            'booking_id': str(booking.id),
            'group_name': booking.group_name,
            'current_participants': booking.current_participants,
            'status': booking.status
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def join_group_booking(request, booking_id):
    """Join an existing group booking."""
    serializer = JoinGroupBookingSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = GroupBookingService()
        result = service.join_booking(booking_id, serializer.validated_data['user_id'])
        
        return Response(result, status=status.HTTP_200_OK)
    
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def process_group_payment(request, booking_id):
    """Process payment for group booking."""
    serializer = ProcessGroupPaymentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = GroupPaymentService()
        result = service.calculate_group_total(
            booking_id,
            serializer.validated_data['base_price']
        )
        
        return Response(result, status=status.HTTP_200_OK)
    
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
