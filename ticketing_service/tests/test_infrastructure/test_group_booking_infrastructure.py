from decimal import Decimal
from django.test import TestCase
import uuid

from domain.group_booking import GroupBooking
from infrastructure.group_booking_pipeline import (
    GroupBookingPipeline,
    GroupPaymentCoordinator,
    GroupAnalytics,
    GroupNotificationSystem
)


class GroupBookingPipelineTest(TestCase):
    """Tests for GroupBookingPipeline."""
    
    def setUp(self):
        self.pipeline = GroupBookingPipeline()
        self.booking = GroupBooking.objects.create(
            event_id=uuid.uuid4(),
            organizer_id=uuid.uuid4(),
            group_name='Pipeline Test',
            min_participants=3,
            max_participants=5,
            current_participants=3
        )
    
    def test_process_complete_booking(self):
        """Test processing complete booking."""
        result = self.pipeline.process(self.booking.id)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['participants'], 3)


class GroupPaymentCoordinatorTest(TestCase):
    """Tests for GroupPaymentCoordinator."""
    
    def setUp(self):
        self.coordinator = GroupPaymentCoordinator()
        self.booking = GroupBooking.objects.create(
            event_id=uuid.uuid4(),
            organizer_id=uuid.uuid4(),
            group_name='Payment Test',
            min_participants=2,
            max_participants=5,
            current_participants=2
        )
    
    def test_coordinate_payment(self):
        """Test coordinating group payment."""
        payments = [
            {'user_id': str(uuid.uuid4()), 'amount': '100.00'},
            {'user_id': str(uuid.uuid4()), 'amount': '100.00'}
        ]
        
        result = self.coordinator.coordinate_payment(self.booking.id, payments)
        
        self.assertEqual(result['total_paid'], '200.00')
        self.assertEqual(result['payment_count'], 2)


class GroupAnalyticsTest(TestCase):
    """Tests for GroupAnalytics."""
    
    def setUp(self):
        self.analytics = GroupAnalytics()
        self.booking = GroupBooking.objects.create(
            event_id=uuid.uuid4(),
            organizer_id=uuid.uuid4(),
            group_name='Analytics Test',
            min_participants=5,
            max_participants=10,
            current_participants=7
        )
    
    def test_track_booking(self):
        """Test tracking booking analytics."""
        result = self.analytics.track_booking(self.booking.id)
        
        self.assertEqual(result['participants'], 7)
        self.assertEqual(result['completion_rate'], 70.0)


class GroupNotificationSystemTest(TestCase):
    """Tests for GroupNotificationSystem."""
    
    def setUp(self):
        self.notification = GroupNotificationSystem()
        self.booking = GroupBooking.objects.create(
            event_id=uuid.uuid4(),
            organizer_id=uuid.uuid4(),
            group_name='Notification Test',
            min_participants=3,
            max_participants=5,
            current_participants=4
        )
    
    def test_notify_participants(self):
        """Test notifying participants."""
        result = self.notification.notify_participants(
            self.booking.id,
            'Group booking confirmed!'
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['recipients'], 4)
