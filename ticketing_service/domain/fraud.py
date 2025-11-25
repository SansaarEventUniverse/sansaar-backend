import uuid
from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class SecurityRule(models.Model):
    """Security rule model for fraud detection."""
    
    RULE_TYPE_CHOICES = [
        ('velocity', 'Velocity Check'),
        ('amount', 'Amount Threshold'),
        ('pattern', 'Pattern Detection'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    rule_type = models.CharField(max_length=20, choices=RULE_TYPE_CHOICES)
    threshold_value = models.DecimalField(max_digits=10, decimal_places=2)
    time_window_minutes = models.IntegerField(default=60)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'security_rules'
    
    def __str__(self):
        return f"{self.name} - {self.rule_type}"
    
    def clean(self):
        """Validate security rule."""
        if self.threshold_value < 0:
            raise ValidationError("Threshold value cannot be negative")
        
        if self.time_window_minutes < 0:
            raise ValidationError("Time window cannot be negative")


class FraudAlert(models.Model):
    """Fraud alert model for suspicious activities."""
    
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
        ('false_positive', 'False Positive'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.UUIDField(db_index=True)
    user_id = models.UUIDField(db_index=True)
    rule_id = models.UUIDField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    description = models.TextField()
    risk_score = models.IntegerField(default=0)
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'fraud_alerts'
        indexes = [
            models.Index(fields=['order_id']),
            models.Index(fields=['user_id']),
            models.Index(fields=['status', 'severity']),
        ]
    
    def __str__(self):
        return f"Alert {self.id} - {self.severity}"
    
    def clean(self):
        """Validate fraud alert."""
        if self.risk_score < 0 or self.risk_score > 100:
            raise ValidationError("Risk score must be between 0 and 100")
    
    def resolve(self, is_fraud: bool = False) -> None:
        """Resolve the alert."""
        if self.status == 'resolved':
            raise ValidationError("Alert is already resolved")
        
        self.status = 'false_positive' if not is_fraud else 'resolved'
        self.resolved_at = timezone.now()
        self.save()
    
    def is_high_risk(self) -> bool:
        """Check if alert is high risk."""
        return self.severity in ['high', 'critical'] and self.risk_score >= 70
