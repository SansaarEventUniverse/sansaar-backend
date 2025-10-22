import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Venue(models.Model):
    """Venue domain model with business logic."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000, blank=True)
    
    # Location
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Capacity
    capacity = models.IntegerField()
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    # Owner
    owner_id = models.UUIDField()
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'venues'
        indexes = [
            models.Index(fields=['owner_id']),
            models.Index(fields=['city']),
            models.Index(fields=['is_verified']),
            models.Index(fields=['deleted_at']),
        ]
    
    def clean(self):
        """Validate venue business rules."""
        errors = {}
        
        if self.capacity and self.capacity < 1:
            errors['capacity'] = 'Capacity must be at least 1'
        
        if self.latitude and (self.latitude < -90 or self.latitude > 90):
            errors['latitude'] = 'Latitude must be between -90 and 90'
        
        if self.longitude and (self.longitude < -180 or self.longitude > 180):
            errors['longitude'] = 'Longitude must be between -180 and 180'
        
        if errors:
            raise ValidationError(errors)
    
    def verify(self):
        """Mark venue as verified."""
        self.is_verified = True
        self.verified_at = timezone.now()
        self.save()
    
    def unverify(self):
        """Remove verification."""
        self.is_verified = False
        self.verified_at = None
        self.save()
    
    def has_coordinates(self):
        """Check if venue has geocoded coordinates."""
        return self.latitude is not None and self.longitude is not None
    
    def soft_delete(self):
        """Soft delete the venue."""
        self.deleted_at = timezone.now()
        self.save()
    
    def __str__(self):
        return f"{self.name} ({self.city})"
