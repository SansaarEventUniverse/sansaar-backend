from typing import List
from django.db.models import Q
import uuid

from domain.venue import Venue


class VenueRepository:
    """Repository for complex venue queries."""
    
    def get_owner_venues(self, owner_id: uuid.UUID) -> List[Venue]:
        """Get all venues for an owner."""
        return list(Venue.objects.filter(
            owner_id=owner_id,
            deleted_at__isnull=True
        ).order_by('-created_at'))
    
    def search_by_location(self, city: str = None, country: str = None) -> List[Venue]:
        """Search venues by location."""
        queryset = Venue.objects.filter(deleted_at__isnull=True)
        
        if city:
            queryset = queryset.filter(city__icontains=city)
        if country:
            queryset = queryset.filter(country__icontains=country)
        
        return list(queryset.order_by('name'))
    
    def get_verified_venues(self) -> List[Venue]:
        """Get all verified venues."""
        return list(Venue.objects.filter(
            is_verified=True,
            deleted_at__isnull=True
        ).order_by('name'))
