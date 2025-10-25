import uuid
from django.test import TestCase

from infrastructure.services.capacity_tracking_service import CapacityTrackingService


class CapacityTrackingServiceTest(TestCase):
    """Tests for CapacityTrackingService."""
    
    def setUp(self):
        self.service = CapacityTrackingService()
        self.event_id = uuid.uuid4()
        
    def test_increment_capacity(self):
        """Test incrementing capacity."""
        count = self.service.increment_capacity(self.event_id)
        self.assertEqual(count, 1)
        
    def test_get_registered_count(self):
        """Test getting registered count."""
        self.service.increment_capacity(self.event_id)
        self.service.increment_capacity(self.event_id)
        count = self.service.get_registered_count(self.event_id)
        self.assertEqual(count, 2)
        
    def test_check_capacity(self):
        """Test checking capacity."""
        self.service.increment_capacity(self.event_id)
        has_capacity = self.service.check_capacity(self.event_id, max_capacity=5)
        self.assertTrue(has_capacity)
