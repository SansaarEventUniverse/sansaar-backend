from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid

from domain.refund import Refund, RefundPolicy


class RefundPolicyModelTest(TestCase):
    """Tests for RefundPolicy model."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
    
    def test_create_refund_policy(self):
        """Test creating a refund policy."""
        policy = RefundPolicy.objects.create(
            event_id=self.event_id,
            refund_allowed=True,
            refund_before_hours=24,
            refund_percentage=Decimal('80.00'),
            processing_fee=Decimal('5.00')
        )
        
        self.assertEqual(policy.refund_percentage, Decimal('80.00'))
        self.assertEqual(policy.processing_fee, Decimal('5.00'))
    
    def test_invalid_percentage_validation(self):
        """Test invalid percentage validation."""
        policy = RefundPolicy(
            event_id=self.event_id,
            refund_percentage=Decimal('150.00')
        )
        
        with self.assertRaises(ValidationError):
            policy.clean()


class RefundModelTest(TestCase):
    """Tests for Refund model."""
    
    def setUp(self):
        self.ticket_id = uuid.uuid4()
        self.order_id = uuid.uuid4()
        
        self.refund = Refund.objects.create(
            ticket_id=self.ticket_id,
            order_id=self.order_id,
            original_amount=Decimal('100.00'),
            refund_amount=Decimal('80.00'),
            reason='Customer request'
        )
    
    def test_create_refund(self):
        """Test creating a refund."""
        self.assertEqual(self.refund.status, 'pending')
        self.assertEqual(self.refund.original_amount, Decimal('100.00'))
        self.assertEqual(self.refund.refund_amount, Decimal('80.00'))
    
    def test_calculate_refund_with_policy(self):
        """Test calculating refund with policy."""
        policy = RefundPolicy.objects.create(
            event_id=uuid.uuid4(),
            refund_percentage=Decimal('80.00'),
            processing_fee=Decimal('5.00')
        )
        
        calculated = self.refund.calculate_refund(policy)
        self.assertEqual(calculated, Decimal('75.00'))  # 100 * 0.8 - 5
    
    def test_process_refund(self):
        """Test processing a refund."""
        self.refund.process()
        self.assertEqual(self.refund.status, 'processing')
    
    def test_complete_refund(self):
        """Test completing a refund."""
        self.refund.process()
        self.refund.complete()
        
        self.assertEqual(self.refund.status, 'completed')
        self.assertIsNotNone(self.refund.processed_at)
    
    def test_reject_refund(self):
        """Test rejecting a refund."""
        self.refund.reject('Policy violation')
        
        self.assertEqual(self.refund.status, 'rejected')
        self.assertEqual(self.refund.rejected_reason, 'Policy violation')
    
    def test_cannot_process_non_pending(self):
        """Test cannot process non-pending refund."""
        self.refund.status = 'completed'
        self.refund.save()
        
        with self.assertRaises(ValidationError):
            self.refund.process()
    
    def test_refund_amount_validation(self):
        """Test refund amount cannot exceed original."""
        refund = Refund(
            ticket_id=uuid.uuid4(),
            order_id=uuid.uuid4(),
            original_amount=Decimal('100.00'),
            refund_amount=Decimal('150.00'),
            reason='Test'
        )
        
        with self.assertRaises(ValidationError):
            refund.clean()
