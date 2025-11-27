from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from application.offline_service import (
    OfflineValidationService,
    TicketSyncService,
    CacheManagementService
)
from presentation.serializers.offline_serializers import (
    ValidateOfflineSerializer,
    SyncTicketDataSerializer,
    OfflineStatusSerializer
)


@api_view(['POST'])
def validate_offline(request):
    """Validate ticket offline."""
    serializer = ValidateOfflineSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = OfflineValidationService()
        result = service.validate_ticket(serializer.validated_data['qr_code'])
        
        return Response(result, status=status.HTTP_200_OK)
    
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def sync_ticket_data(request):
    """Sync ticket data for offline use."""
    serializer = SyncTicketDataSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = TicketSyncService()
        result = service.sync_tickets(
            serializer.validated_data['event_id'],
            serializer.validated_data['tickets']
        )
        
        return Response(result, status=status.HTTP_200_OK)
    
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def offline_status(request, event_id):
    """Get offline status for event."""
    try:
        cache_service = CacheManagementService()
        cache = cache_service.get_cache(event_id)
        
        data = {
            'event_id': str(cache.event_id),
            'ticket_count': cache.ticket_count,
            'last_synced': cache.last_synced,
            'cache_status': 'active' if not cache.is_expired() else 'expired'
        }
        
        serializer = OfflineStatusSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
