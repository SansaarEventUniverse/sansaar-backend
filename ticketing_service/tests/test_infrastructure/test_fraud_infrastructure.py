from django.test import TestCase
import uuid

from domain.fraud import FraudAlert, SecurityRule
from infrastructure.repositories.fraud_repository import (
    FraudRepository,
    FraudDetectionEngine
)


class FraudRepositoryTest(TestCase):
    """Tests for FraudRepository."""
    
    def setUp(self):
        self.repository = FraudRepository()
        
        rule = SecurityRule.objects.create(
            name='Test Rule',
            rule_type='velocity',
            threshold_value=5
        )
        
        FraudAlert.objects.create(
            order_id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            rule_id=rule.id,
            severity='high',
            description='Test',
            risk_score=80
        )
    
    def test_get_open_alerts(self):
        """Test getting open alerts."""
        alerts = self.repository.get_open_alerts()
        self.assertEqual(len(alerts), 1)
    
    def test_get_fraud_analytics(self):
        """Test getting fraud analytics."""
        analytics = self.repository.get_fraud_analytics()
        
        self.assertEqual(analytics['total_alerts'], 1)
        self.assertEqual(analytics['open_alerts'], 1)


class FraudDetectionEngineTest(TestCase):
    """Tests for FraudDetectionEngine."""
    
    def test_calculate_risk_score(self):
        """Test risk score calculation."""
        factors = {'velocity': 30, 'amount': 40}
        score = FraudDetectionEngine.calculate_risk_score(factors)
        
        self.assertEqual(score, 70)
    
    def test_is_suspicious_pattern(self):
        """Test suspicious pattern detection."""
        self.assertTrue(FraudDetectionEngine.is_suspicious_pattern(10, 24))
        self.assertFalse(FraudDetectionEngine.is_suspicious_pattern(3, 24))
