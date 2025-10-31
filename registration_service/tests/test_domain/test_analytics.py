import uuid
from decimal import Decimal
from django.test import TestCase

from domain.analytics import RegistrationAnalytics


class RegistrationAnalyticsModelTest(TestCase):
    """Tests for RegistrationAnalytics model."""
    
    def test_create_analytics(self):
        """Test creating analytics record."""
        analytics = RegistrationAnalytics.objects.create(
            event_id=uuid.uuid4(),
            total_registrations=100,
            confirmed_registrations=80,
        )
        self.assertIsNotNone(analytics.id)
        
    def test_calculate_utilization(self):
        """Test capacity utilization calculation."""
        analytics = RegistrationAnalytics(
            event_id=uuid.uuid4(),
            confirmed_registrations=75,
        )
        utilization = analytics.calculate_utilization(100)
        self.assertEqual(utilization, Decimal('75.00'))
        
    def test_get_conversion_rate(self):
        """Test waitlist conversion rate."""
        analytics = RegistrationAnalytics(
            event_id=uuid.uuid4(),
            total_waitlist=20,
            promoted_from_waitlist=10,
        )
        rate = analytics.get_conversion_rate()
        self.assertEqual(rate, Decimal('50.00'))
