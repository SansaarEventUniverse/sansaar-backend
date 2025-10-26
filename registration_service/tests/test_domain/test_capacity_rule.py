import uuid
from django.test import TestCase
from django.core.exceptions import ValidationError

from domain.capacity_rule import CapacityRule


class CapacityRuleModelTest(TestCase):
    """Tests for CapacityRule domain model."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
        
    def test_create_capacity_rule(self):
        """Test creating a capacity rule."""
        rule = CapacityRule.objects.create(
            event_id=self.event_id,
            max_capacity=100,
            warning_threshold=80,
        )
        self.assertIsNotNone(rule.id)
        self.assertEqual(rule.max_capacity, 100)
        
    def test_is_at_capacity(self):
        """Test capacity check."""
        rule = CapacityRule.objects.create(
            event_id=self.event_id,
            max_capacity=100,
            warning_threshold=80,
        )
        self.assertTrue(rule.is_at_capacity(100))
        self.assertFalse(rule.is_at_capacity(99))
        
    def test_is_near_capacity(self):
        """Test near capacity threshold."""
        rule = CapacityRule.objects.create(
            event_id=self.event_id,
            max_capacity=100,
            warning_threshold=80,
        )
        self.assertTrue(rule.is_near_capacity(80))
        self.assertFalse(rule.is_near_capacity(79))
        
    def test_available_spots(self):
        """Test available spots calculation."""
        rule = CapacityRule.objects.create(
            event_id=self.event_id,
            max_capacity=100,
            warning_threshold=80,
        )
        self.assertEqual(rule.available_spots(70), 30)
        self.assertEqual(rule.available_spots(100), 0)
