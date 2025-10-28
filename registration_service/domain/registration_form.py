import uuid
from django.db import models
from django.core.exceptions import ValidationError


class RegistrationForm(models.Model):
    """Registration form model for custom event forms."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField(unique=True)
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'registration_forms'
        indexes = [
            models.Index(fields=['event_id']),
        ]
    
    def __str__(self):
        return f"{self.title} - Event {self.event_id}"


class CustomField(models.Model):
    """Custom field model for dynamic form fields."""
    
    FIELD_TYPES = [
        ('text', 'Text'),
        ('email', 'Email'),
        ('number', 'Number'),
        ('textarea', 'Textarea'),
        ('select', 'Select'),
        ('checkbox', 'Checkbox'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    form = models.ForeignKey(RegistrationForm, on_delete=models.CASCADE, related_name='fields')
    
    label = models.CharField(max_length=255)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    is_required = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    # Field options (for select fields)
    options = models.JSONField(null=True, blank=True)
    
    # Validation
    min_length = models.IntegerField(null=True, blank=True)
    max_length = models.IntegerField(null=True, blank=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'custom_fields'
        indexes = [
            models.Index(fields=['form', 'order']),
        ]
        ordering = ['order']
    
    def clean(self):
        """Validate custom field."""
        errors = {}
        
        if self.field_type == 'select' and not self.options:
            errors['options'] = 'Select fields must have options'
        
        if self.min_length and self.max_length and self.min_length > self.max_length:
            errors['min_length'] = 'Min length cannot be greater than max length'
        
        if errors:
            raise ValidationError(errors)
    
    def __str__(self):
        return f"{self.label} ({self.field_type})"
