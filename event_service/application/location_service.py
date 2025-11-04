from typing import List, Dict, Any
import uuid

from domain.location import EventLocation, LocationSearch


class LocationSearchService:
    """Service for location-based event search."""
    
    def search_nearby(self, latitude: float, longitude: float, 
                     radius_km: float = 10.0) -> List[Dict[str, Any]]:
        """Search for events within radius of coordinates."""
        locations = EventLocation.objects.all()
        
        nearby = []
        for loc in locations:
            distance = loc.distance_to(latitude, longitude)
            if distance <= radius_km:
                nearby.append({
                    'event_id': str(loc.event_id),
                    'city': loc.city,
                    'country': loc.country,
                    'latitude': loc.latitude,
                    'longitude': loc.longitude,
                    'distance_km': round(distance, 2),
                })
        
        # Sort by distance
        nearby.sort(key=lambda x: x['distance_km'])
        return nearby


class NearbyEventsService:
    """Service for finding nearby events."""
    
    def execute(self, city: str, radius_km: float = 50.0) -> List[EventLocation]:
        """Find events near a city."""
        # Get events in the city
        city_events = EventLocation.objects.filter(city__iexact=city)
        
        if not city_events.exists():
            return []
        
        # Use first event's coordinates as reference
        ref_location = city_events.first()
        
        # Find all events within radius
        search_service = LocationSearchService()
        nearby = search_service.search_nearby(
            ref_location.latitude,
            ref_location.longitude,
            radius_km
        )
        
        return nearby


class GeoFilterService:
    """Service for geo-filtering events."""
    
    def filter_by_city(self, city: str) -> List[EventLocation]:
        """Filter events by city."""
        return list(EventLocation.objects.filter(city__iexact=city))
    
    def filter_by_country(self, country: str) -> List[EventLocation]:
        """Filter events by country."""
        return list(EventLocation.objects.filter(country__iexact=country))
    
    def filter_by_bounds(self, min_lat: float, max_lat: float,
                        min_lon: float, max_lon: float) -> List[EventLocation]:
        """Filter events within geographic bounds."""
        return list(
            EventLocation.objects.filter(
                latitude__gte=min_lat,
                latitude__lte=max_lat,
                longitude__gte=min_lon,
                longitude__lte=max_lon,
            )
        )
