import uuid
from decimal import Decimal
from typing import Dict, Any
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

from domain.fraud import SecurityRule, FraudAlert
from domain.order import Order


class FraudDetectionService:
    """Service for detecting fraudulent activities."""
    
    def check_order(self, order: Order) -> FraudAlert:
        """Check order for fraud."""
        risk_score = 0
        alerts = []
        
        # Check velocity (multiple orders in short time)
        recent_orders = Order.objects.filter(
            user_id=order.user_id,
            created_at__gte=timezone.now() - timedelta(hours=1)
        ).count()
        
        if recent_orders > 5:
            risk_score += 30
            alerts.append('High velocity detected')
        
        # Check amount threshold
        if order.total_amount > Decimal('1000.00'):
            risk_score += 20
            alerts.append('High amount transaction')
        
        # Determine severity
        if risk_score >= 70:
            severity = 'critical'
        elif risk_score >= 50:
            severity = 'high'
        elif risk_score >= 30:
            severity = 'medium'
        else:
            severity = 'low'
        
        # Create alert if risk detected
        if risk_score > 0:
            rule = SecurityRule.objects.filter(is_active=True).first()
            if not rule:
                rule = SecurityRule.objects.create(
                    name='Default Rule',
                    rule_type='pattern',
                    threshold_value=Decimal('50.00')
                )
            
            alert = FraudAlert.objects.create(
                order_id=order.id,
                user_id=order.user_id,
                rule_id=rule.id,
                severity=severity,
                description='; '.join(alerts),
                risk_score=risk_score
            )
            
            return alert
        
        return None


class SecurityValidationService:
    """Service for security validation."""
    
    def validate_order(self, order: Order) -> Dict[str, Any]:
        """Validate order security."""
        issues = []
        
        # Check for suspicious patterns
        if order.total_amount == Decimal('0.00'):
            issues.append('Zero amount order')
        
        # Check user history
        user_orders = Order.objects.filter(user_id=order.user_id).count()
        if user_orders == 1:
            issues.append('First time user')
        
        is_valid = len(issues) == 0
        
        return {
            'is_valid': is_valid,
            'issues': issues,
            'risk_level': 'high' if not is_valid else 'low'
        }


class RiskAssessmentService:
    """Service for risk assessment."""
    
    def assess_order(self, order: Order) -> Dict[str, Any]:
        """Assess order risk."""
        risk_factors = []
        risk_score = 0
        
        # Check order amount
        if order.total_amount > Decimal('500.00'):
            risk_factors.append('High value order')
            risk_score += 25
        
        # Check user activity
        recent_orders = Order.objects.filter(
            user_id=order.user_id,
            created_at__gte=timezone.now() - timedelta(days=1)
        ).count()
        
        if recent_orders > 3:
            risk_factors.append('Multiple recent orders')
            risk_score += 35
        
        # Check for existing alerts
        existing_alerts = FraudAlert.objects.filter(
            user_id=order.user_id,
            status='open'
        ).count()
        
        if existing_alerts > 0:
            risk_factors.append('Existing fraud alerts')
            risk_score += 40
        
        return {
            'order_id': order.id,
            'risk_score': min(risk_score, 100),
            'risk_factors': risk_factors,
            'recommendation': 'block' if risk_score >= 70 else 'review' if risk_score >= 40 else 'approve'
        }
