import uuid
import hashlib
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Ticket(models.Model):
    """Ticket model with QR code generation."""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('used', 'Used'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket_type_id = models.UUIDField(db_index=True)
    order_id = models.UUIDField(db_index=True)
    attendee_name = models.CharField(max_length=200)
    attendee_email = models.EmailField()
    qr_code_data = models.CharField(max_length=500, unique=True)
    security_hash = models.CharField(max_length=64)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    checked_in_at = models.DateTimeField(null=True, blank=True)
    checked_in_by = models.UUIDField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tickets'
        indexes = [
            models.Index(fields=['ticket_type_id', 'status']),
            models.Index(fields=['order_id']),
            models.Index(fields=['qr_code_data']),
        ]
    
    def __str__(self):
        return f"Ticket {self.id} - {self.attendee_name}"
    
    def generate_qr_data(self) -> str:
        """Generate QR code data string."""
        return f"{self.id}|{self.ticket_type_id}|{self.order_id}"
    
    def generate_security_hash(self) -> str:
        """Generate security hash for anti-fraud."""
        data = f"{self.id}{self.ticket_type_id}{self.order_id}{self.attendee_email}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def validate_security_hash(self, provided_hash: str) -> bool:
        """Validate security hash."""
        return self.security_hash == provided_hash
    
    def can_check_in(self) -> bool:
        """Check if ticket can be checked in."""
        return self.status == 'active' and self.checked_in_at is None
    
    def check_in(self, checked_in_by: uuid.UUID) -> None:
        """Check in the ticket."""
        if not self.can_check_in():
            raise ValidationError("Ticket cannot be checked in")
        
        self.status = 'used'
        self.checked_in_at = timezone.now()
        self.checked_in_by = checked_in_by
        self.save()
    
    def cancel(self) -> None:
        """Cancel the ticket."""
        if self.status == 'used':
            raise ValidationError("Cannot cancel used ticket")
        
        self.status = 'cancelled'
        self.save()
    
    def is_valid(self) -> bool:
        """Check if ticket is valid for use."""
        return self.status == 'active'
    
    def save(self, *args, **kwargs):
        """Override save to generate QR data and security hash."""
        if not self.qr_code_data:
            self.qr_code_data = self.generate_qr_data()
        if not self.security_hash:
            self.security_hash = self.generate_security_hash()
        super().save(*args, **kwargs)
