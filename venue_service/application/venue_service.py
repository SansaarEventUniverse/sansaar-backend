from typing import Dict, Any, List
import uuid
from django.core.exceptions import ValidationError

from domain.venue import Venue


class CreateVenueService:
    """Service for creating venues."""
    
    def execute(self, data: Dict[str, Any]) -> Venue:
        """Create a new venue."""
        venue = Venue(
            name=data['name'],
            description=data.get('description', ''),
            address=data['address'],
            city=data['city'],
            state=data['state'],
            country=data['country'],
            postal_code=data['postal_code'],
            capacity=data['capacity'],
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            owner_id=data['owner_id'],
        )
        venue.clean()
        venue.save()
        return venue


class UpdateVenueService:
    """Service for updating venues."""
    
    def execute(self, venue_id: uuid.UUID, data: Dict[str, Any]) -> Venue:
        """Update an existing venue."""
        try:
            venue = Venue.objects.get(id=venue_id, deleted_at__isnull=True)
        except Venue.DoesNotExist:
            raise ValidationError('Venue not found')
        
        for field, value in data.items():
            if hasattr(venue, field):
                setattr(venue, field, value)
        
        venue.clean()
        venue.save()
        return venue


class SearchVenueService:
    """Service for searching venues."""
    
    def execute(self, city: str = None, country: str = None, 
                verified_only: bool = False) -> List[Venue]:
        """Search venues by criteria."""
        queryset = Venue.objects.filter(deleted_at__isnull=True)
        
        if city:
            queryset = queryset.filter(city__icontains=city)
        
        if country:
            queryset = queryset.filter(country__icontains=country)
        
        if verified_only:
            queryset = queryset.filter(is_verified=True)
        
        return list(queryset.order_by('-created_at'))


class GetVenueService:
    """Service for retrieving venues."""
    
    def execute(self, venue_id: uuid.UUID) -> Venue:
        """Get venue by ID."""
        try:
            return Venue.objects.get(id=venue_id, deleted_at__isnull=True)
        except Venue.DoesNotExist:
            raise ValidationError('Venue not found')
