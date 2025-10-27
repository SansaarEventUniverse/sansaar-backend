import uuid
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from application.capacity_service import (
    CapacityManagementService,
    CreateCapacityRuleService,
)
from presentation.serializers.capacity_serializers import CapacityRuleSerializer


@api_view(['GET'])
def get_capacity(request, event_id):
    """Get capacity information for an event."""
    try:
        service = CapacityManagementService()
        result = service.execute(uuid.UUID(event_id))
        
        return Response(result)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_capacity_rule(request, event_id):
    """Create capacity rule for an event."""
    try:
        data = request.data.copy()
        data['event_id'] = uuid.UUID(event_id)
        
        service = CreateCapacityRuleService()
        rule = service.execute(data)
        
        return Response(
            CapacityRuleSerializer(rule).data,
            status=status.HTTP_201_CREATED
        )
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)
