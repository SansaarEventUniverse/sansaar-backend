import uuid
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from application.registration_service import (
    RegisterForEventService,
    CancelRegistrationService,
    CheckCapacityService,
)
from infrastructure.repositories.registration_repository import RegistrationRepository
from presentation.serializers.registration_serializers import RegistrationSerializer


@api_view(['POST'])
def register_for_event(request, event_id):
    """Register for an event."""
    try:
        data = request.data.copy()
        data['event_id'] = uuid.UUID(event_id)
        
        service = RegisterForEventService()
        registration = service.execute(data)
        
        return Response(
            RegistrationSerializer(registration).data,
            status=status.HTTP_201_CREATED
        )
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def cancel_registration(request, event_id):
    """Cancel a registration."""
    user_id = request.data.get('user_id')
    if not user_id:
        return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = CancelRegistrationService()
        registration = service.execute(uuid.UUID(event_id), uuid.UUID(user_id))
        
        return Response(RegistrationSerializer(registration).data)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({'error': 'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_event_registrations(request, event_id):
    """Get all registrations for an event."""
    try:
        repository = RegistrationRepository()
        registrations = repository.get_event_registrations(uuid.UUID(event_id))
        
        return Response({
            'count': len(registrations),
            'results': RegistrationSerializer(registrations, many=True).data
        })
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def check_capacity(request, event_id):
    """Check event capacity."""
    max_capacity = request.query_params.get('max_capacity')
    if not max_capacity:
        return Response({'error': 'max_capacity is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = CheckCapacityService()
        result = service.execute(uuid.UUID(event_id), int(max_capacity))
        
        return Response(result)
    except ValueError:
        return Response({'error': 'Invalid parameters'}, status=status.HTTP_400_BAD_REQUEST)
