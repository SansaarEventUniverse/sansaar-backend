from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
import uuid

from domain.revenue import Revenue, RevenueReport
from domain.order import Order
from infrastructure.repositories.revenue_repository import (
    RevenueRepository,
    RevenueTracker
)


class RevenueRepositoryTest(TestCase):
    """Tests for RevenueRepository."""
    
    def setUp(self):
        self.repository = RevenueRepository()
        self.event_id = uuid.uuid4()
        
        order = Order.objects.create(
            user_id=uuid.uuid4(),
            event_id=self.event_id,
            total_amount=Decimal('100.00'),
            status='confirmed'
        )
        
        Revenue.objects.create(
            event_id=self.event_id,
            order_id=order.id,
            gross_amount=Decimal('100.00'),
            platform_fee=Decimal('10.00'),
            payment_fee=Decimal('3.00')
        )
    
    def test_get_event_revenue(self):
        """Test getting event revenue."""
        revenues = self.repository.get_event_revenue(self.event_id)
        self.assertEqual(len(revenues), 1)
    
    def test_get_revenue_analytics(self):
        """Test getting revenue analytics."""
        analytics = self.repository.get_revenue_analytics(self.event_id)
        
        self.assertEqual(analytics['total_gross'], Decimal('100.00'))
        self.assertEqual(analytics['total_net'], Decimal('87.00'))
        self.assertEqual(analytics['total_orders'], 1)


class RevenueTrackerTest(TestCase):
    """Tests for RevenueTracker."""
    
    def test_track_order_revenue(self):
        """Test tracking order revenue."""
        event_id = uuid.uuid4()
        order_id = uuid.uuid4()
        
        revenue = RevenueTracker.track_order_revenue(
            event_id,
            order_id,
            Decimal('100.00')
        )
        
        self.assertEqual(revenue.gross_amount, Decimal('100.00'))
        self.assertEqual(revenue.platform_fee, Decimal('10.00'))
        self.assertGreater(revenue.payment_fee, Decimal('0.00'))
