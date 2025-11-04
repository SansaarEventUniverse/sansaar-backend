import uuid
from django.db import models
from math import radians, cos, sin, asin, sqrt


class LocationSearch(models.Model):
    """Model for location-based search criteria."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Location
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    # Search parameters
    radius_km = models.FloatField(default=10.0)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'location_searches'
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['country']),
            models.Index(fields=['latitude', 'longitude']),
        ]
    
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points using Haversine formula (in km)."""
        # Convert to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        
        # Radius of earth in kilometers
        r = 6371
        
        return c * r
    
    def __str__(self):
        return f"Search at ({self.latitude}, {self.longitude}) within {self.radius_km}km"


class EventLocation(models.Model):
    """Extended location information for events."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField(unique=True)
    
    # Address
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Coordinates
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    # Metadata
    is_verified = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'event_locations'
        indexes = [
            models.Index(fields=['event_id']),
            models.Index(fields=['city']),
            models.Index(fields=['country']),
            models.Index(fields=['latitude', 'longitude']),
        ]
    
    def distance_to(self, lat: float, lon: float) -> float:
        """Calculate distance to given coordinates."""
        return LocationSearch.calculate_distance(
            self.latitude, self.longitude, lat, lon
        )
    
    def __str__(self):
        return f"{self.city}, {self.country}"
