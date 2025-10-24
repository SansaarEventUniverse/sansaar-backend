import uuid
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from application.venue_service import (
    CreateVenueService,
    UpdateVenueService,
    SearchVenueService,
    GetVenueService,
)
from presentation.serializers.venue_serializers import VenueSerializer


@api_view(['POST'])
def create_venue(request):
    """Create a new venue."""
    serializer = VenueSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = CreateVenueService()
        venue = service.execute(serializer.validated_data)
        return Response(
            VenueSerializer(venue).data,
            status=status.HTTP_201_CREATED
        )
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_venue(request, venue_id):
    """Get venue by ID."""
    try:
        service = GetVenueService()
        venue = service.execute(uuid.UUID(venue_id))
        return Response(VenueSerializer(venue).data)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({'error': 'Invalid venue ID'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
def update_venue(request, venue_id):
    """Update a venue."""
    try:
        service = UpdateVenueService()
        venue = service.execute(uuid.UUID(venue_id), request.data)
        return Response(VenueSerializer(venue).data)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'error': 'Invalid venue ID'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search_venues(request):
    """Search venues."""
    city = request.query_params.get('city')
    country = request.query_params.get('country')
    verified_only = request.query_params.get('verified', 'false').lower() == 'true'
    
    service = SearchVenueService()
    venues = service.execute(city=city, country=country, verified_only=verified_only)
    
    return Response({
        'count': len(venues),
        'results': VenueSerializer(venues, many=True).data
    })
