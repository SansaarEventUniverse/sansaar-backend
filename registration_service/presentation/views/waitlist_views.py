import uuid
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from application.waitlist_service import (
    JoinWaitlistService,
    LeaveWaitlistService,
    GetWaitlistPositionService,
)
from infrastructure.repositories.waitlist_repository import WaitlistRepository
from presentation.serializers.waitlist_serializers import WaitlistSerializer


@api_view(['POST'])
def join_waitlist(request, event_id):
    """Join event waitlist."""
    try:
        data = request.data.copy()
        data['event_id'] = uuid.UUID(event_id)
        
        service = JoinWaitlistService()
        waitlist = service.execute(data)
        
        return Response(
            WaitlistSerializer(waitlist).data,
            status=status.HTTP_201_CREATED
        )
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def leave_waitlist(request, event_id):
    """Leave event waitlist."""
    user_id = request.data.get('user_id')
    if not user_id:
        return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = LeaveWaitlistService()
        waitlist = service.execute(uuid.UUID(event_id), uuid.UUID(user_id))
        
        return Response({'message': 'Left waitlist successfully'})
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({'error': 'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_waitlist_position(request, event_id):
    """Get user's waitlist position."""
    user_id = request.query_params.get('user_id')
    if not user_id:
        return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = GetWaitlistPositionService()
        result = service.execute(uuid.UUID(event_id), uuid.UUID(user_id))
        
        return Response(result)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({'error': 'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_event_waitlist(request, event_id):
    """Get all waitlist entries for an event."""
    try:
        repository = WaitlistRepository()
        waitlist = repository.get_event_waitlist(uuid.UUID(event_id))
        
        return Response({
            'count': len(waitlist),
            'results': WaitlistSerializer(waitlist, many=True).data
        })
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)
