from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
import uuid

from domain.fraud import SecurityRule, FraudAlert
from domain.order import Order
from application.fraud_service import (
    FraudDetectionService,
    SecurityValidationService,
    RiskAssessmentService
)


class FraudDetectionServiceTest(TestCase):
    """Tests for FraudDetectionService."""
    
    def setUp(self):
        self.service = FraudDetectionService()
        self.user_id = uuid.uuid4()
        self.event_id = uuid.uuid4()
    
    def test_check_order_high_amount(self):
        """Test fraud detection for high amount."""
        order = Order.objects.create(
            user_id=self.user_id,
            event_id=self.event_id,
            total_amount=Decimal('1500.00'),
            status='pending'
        )
        
        alert = self.service.check_order(order)
        
        self.assertIsNotNone(alert)
        self.assertGreater(alert.risk_score, 0)
    
    def test_check_order_normal(self):
        """Test fraud detection for normal order."""
        order = Order.objects.create(
            user_id=self.user_id,
            event_id=self.event_id,
            total_amount=Decimal('50.00'),
            status='pending'
        )
        
        alert = self.service.check_order(order)
        
        self.assertIsNone(alert)


class SecurityValidationServiceTest(TestCase):
    """Tests for SecurityValidationService."""
    
    def setUp(self):
        self.service = SecurityValidationService()
        self.user_id = uuid.uuid4()
        self.event_id = uuid.uuid4()
    
    def test_validate_order(self):
        """Test order validation."""
        order = Order.objects.create(
            user_id=self.user_id,
            event_id=self.event_id,
            total_amount=Decimal('100.00'),
            status='pending'
        )
        
        result = self.service.validate_order(order)
        
        self.assertIn('is_valid', result)
        self.assertIn('issues', result)


class RiskAssessmentServiceTest(TestCase):
    """Tests for RiskAssessmentService."""
    
    def setUp(self):
        self.service = RiskAssessmentService()
        self.user_id = uuid.uuid4()
        self.event_id = uuid.uuid4()
    
    def test_assess_order(self):
        """Test order risk assessment."""
        order = Order.objects.create(
            user_id=self.user_id,
            event_id=self.event_id,
            total_amount=Decimal('600.00'),
            status='pending'
        )
        
        assessment = self.service.assess_order(order)
        
        self.assertIn('risk_score', assessment)
        self.assertIn('recommendation', assessment)
        self.assertGreater(assessment['risk_score'], 0)
