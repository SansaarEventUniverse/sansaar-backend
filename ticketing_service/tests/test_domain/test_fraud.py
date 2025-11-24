from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
import uuid

from domain.fraud import SecurityRule, FraudAlert


class SecurityRuleModelTest(TestCase):
    """Tests for SecurityRule model."""
    
    def test_create_security_rule(self):
        """Test creating a security rule."""
        rule = SecurityRule.objects.create(
            name='Velocity Check',
            rule_type='velocity',
            threshold_value=Decimal('5.00'),
            time_window_minutes=60
        )
        
        self.assertEqual(rule.rule_type, 'velocity')
        self.assertTrue(rule.is_active)
    
    def test_negative_threshold_validation(self):
        """Test negative threshold validation."""
        rule = SecurityRule(
            name='Invalid',
            rule_type='amount',
            threshold_value=Decimal('-10.00')
        )
        
        with self.assertRaises(ValidationError):
            rule.clean()


class FraudAlertModelTest(TestCase):
    """Tests for FraudAlert model."""
    
    def setUp(self):
        self.order_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        self.rule_id = uuid.uuid4()
    
    def test_create_fraud_alert(self):
        """Test creating a fraud alert."""
        alert = FraudAlert.objects.create(
            order_id=self.order_id,
            user_id=self.user_id,
            rule_id=self.rule_id,
            severity='high',
            description='Suspicious activity detected',
            risk_score=85
        )
        
        self.assertEqual(alert.status, 'open')
        self.assertEqual(alert.risk_score, 85)
    
    def test_resolve_alert(self):
        """Test resolving an alert."""
        alert = FraudAlert.objects.create(
            order_id=self.order_id,
            user_id=self.user_id,
            rule_id=self.rule_id,
            severity='medium',
            description='Test',
            risk_score=50
        )
        
        alert.resolve(is_fraud=False)
        self.assertEqual(alert.status, 'false_positive')
        self.assertIsNotNone(alert.resolved_at)
    
    def test_is_high_risk(self):
        """Test high risk detection."""
        alert = FraudAlert.objects.create(
            order_id=self.order_id,
            user_id=self.user_id,
            rule_id=self.rule_id,
            severity='critical',
            description='Test',
            risk_score=90
        )
        
        self.assertTrue(alert.is_high_risk())
    
    def test_risk_score_validation(self):
        """Test risk score validation."""
        alert = FraudAlert(
            order_id=self.order_id,
            user_id=self.user_id,
            rule_id=self.rule_id,
            severity='low',
            description='Test',
            risk_score=150
        )
        
        with self.assertRaises(ValidationError):
            alert.clean()
