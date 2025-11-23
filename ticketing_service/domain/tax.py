import uuid
from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError


class TaxRule(models.Model):
    """Tax rule model for different jurisdictions."""
    
    TAX_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=2, default='US')
    state = models.CharField(max_length=50, blank=True)
    tax_type = models.CharField(max_length=20, choices=TAX_TYPE_CHOICES, default='percentage')
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tax_rules'
        indexes = [
            models.Index(fields=['country', 'state']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.tax_rate}%"
    
    def clean(self):
        """Validate tax rule."""
        if self.tax_rate < 0:
            raise ValidationError("Tax rate cannot be negative")
        
        if self.tax_type == 'percentage' and self.tax_rate > 100:
            raise ValidationError("Percentage tax rate cannot exceed 100")
    
    def calculate_tax(self, amount: Decimal) -> Decimal:
        """Calculate tax amount."""
        if self.tax_type == 'percentage':
            return (amount * self.tax_rate / 100).quantize(Decimal('0.01'))
        return self.tax_rate


class TaxCalculation(models.Model):
    """Tax calculation model for orders."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.UUIDField(db_index=True)
    tax_rule_id = models.UUIDField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tax_calculations'
        indexes = [
            models.Index(fields=['order_id']),
        ]
    
    def __str__(self):
        return f"Tax {self.id} - {self.tax_amount}"
    
    def clean(self):
        """Validate tax calculation."""
        if self.subtotal < 0:
            raise ValidationError("Subtotal cannot be negative")
        
        if self.tax_amount < 0:
            raise ValidationError("Tax amount cannot be negative")
    
    def calculate_total(self) -> Decimal:
        """Calculate total with tax."""
        return self.subtotal + self.tax_amount
    
    def save(self, *args, **kwargs):
        """Calculate total before saving."""
        self.total = self.calculate_total()
        super().save(*args, **kwargs)
