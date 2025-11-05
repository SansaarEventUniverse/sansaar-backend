from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from application.location_service import (
    LocationSearchService,
    NearbyEventsService,
    GeoFilterService,
)
from presentation.serializers.location_serializers import (
    NearbySearchSerializer,
    LocationSearchSerializer,
)


@api_view(['GET'])
def search_nearby(request):
    """Search for events near coordinates."""
    serializer = NearbySearchSerializer(data=request.GET)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    service = LocationSearchService()
    results = service.search_nearby(
        serializer.validated_data['latitude'],
        serializer.validated_data['longitude'],
        serializer.validated_data.get('radius_km', 10.0)
    )
    
    return Response({
        'results': results,
        'count': len(results)
    })


@api_view(['GET'])
def search_by_location(request):
    """Search events by location (city/country)."""
    city = request.GET.get('city')
    country = request.GET.get('country')
    
    service = GeoFilterService()
    
    if city:
        results = service.filter_by_city(city)
    elif country:
        results = service.filter_by_country(country)
    else:
        return Response(
            {'error': 'Please provide city or country'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return Response({
        'results': [
            {
                'event_id': str(loc.event_id),
                'city': loc.city,
                'country': loc.country,
                'latitude': loc.latitude,
                'longitude': loc.longitude,
            }
            for loc in results
        ],
        'count': len(results)
    })


@api_view(['GET'])
def get_map_events(request):
    """Get events for map display within bounds."""
    try:
        min_lat = float(request.GET.get('min_lat'))
        max_lat = float(request.GET.get('max_lat'))
        min_lon = float(request.GET.get('min_lon'))
        max_lon = float(request.GET.get('max_lon'))
    except (TypeError, ValueError):
        return Response(
            {'error': 'Invalid coordinates'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    service = GeoFilterService()
    results = service.filter_by_bounds(min_lat, max_lat, min_lon, max_lon)
    
    return Response({
        'events': [
            {
                'event_id': str(loc.event_id),
                'city': loc.city,
                'latitude': loc.latitude,
                'longitude': loc.longitude,
            }
            for loc in results
        ],
        'count': len(results)
    })
