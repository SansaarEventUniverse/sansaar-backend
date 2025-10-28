import uuid
from django.db import models
from django.core.exceptions import ValidationError


class GroupRegistration(models.Model):
    """Group registration model for event group bookings."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField()
    
    group_name = models.CharField(max_length=255)
    group_leader_id = models.UUIDField()
    group_leader_email = models.EmailField()
    
    min_size = models.IntegerField(default=2)
    max_size = models.IntegerField()
    current_size = models.IntegerField(default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Pricing
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'group_registrations'
        indexes = [
            models.Index(fields=['event_id']),
            models.Index(fields=['group_leader_id']),
        ]
    
    def clean(self):
        """Validate group registration."""
        errors = {}
        
        if self.min_size < 2:
            errors['min_size'] = 'Minimum group size must be at least 2'
        
        if self.max_size < self.min_size:
            errors['max_size'] = 'Max size cannot be less than min size'
        
        if self.current_size > self.max_size:
            errors['current_size'] = 'Current size exceeds max size'
        
        if errors:
            raise ValidationError(errors)
    
    def is_full(self) -> bool:
        """Check if group is full."""
        return self.current_size >= self.max_size
    
    def can_add_members(self, count: int = 1) -> bool:
        """Check if members can be added."""
        return self.current_size + count <= self.max_size
    
    def calculate_total(self) -> None:
        """Calculate total amount."""
        self.total_amount = self.price_per_person * self.current_size
    
    def __str__(self):
        return f"{self.group_name} - {self.current_size}/{self.max_size}"


class GroupMember(models.Model):
    """Group member model for tracking individual members."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(GroupRegistration, on_delete=models.CASCADE, related_name='members')
    
    user_id = models.UUIDField()
    name = models.CharField(max_length=255)
    email = models.EmailField()
    
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'group_members'
        unique_together = [['group', 'user_id']]
        indexes = [
            models.Index(fields=['group', 'user_id']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.group.group_name}"
