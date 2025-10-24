import googlemaps
from django.conf import settings
from typing import Optional, Tuple


class GeocodingService:
    """Service for geocoding addresses using Google Maps API."""
    
    def __init__(self):
        self.client = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    
    def geocode_address(self, address: str) -> Optional[Tuple[float, float]]:
        """Geocode an address and return (latitude, longitude)."""
        try:
            result = self.client.geocode(address)
            if result:
                location = result[0]['geometry']['location']
                return (location['lat'], location['lng'])
        except Exception:
            pass
        return None
