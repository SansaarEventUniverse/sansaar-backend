import uuid
from django.test import TestCase
from django.core.exceptions import ValidationError

from application.capacity_service import (
    CapacityManagementService,
    CreateCapacityRuleService,
)
from domain.capacity_rule import CapacityRule
from domain.registration import Registration


class CapacityManagementServiceTest(TestCase):
    """Tests for CapacityManagementService."""
    
    def setUp(self):
        self.service = CapacityManagementService()
        self.event_id = uuid.uuid4()
        
    def test_get_capacity_info(self):
        """Test getting capacity information."""
        CapacityRule.objects.create(
            event_id=self.event_id,
            max_capacity=100,
            warning_threshold=80,
        )
        
        # Create some registrations
        for i in range(3):
            Registration.objects.create(
                event_id=self.event_id,
                user_id=uuid.uuid4(),
                attendee_name=f'User {i}',
                attendee_email=f'user{i}@example.com',
            )
        
        result = self.service.execute(self.event_id)
        self.assertEqual(result['max_capacity'], 100)
        self.assertEqual(result['confirmed_count'], 3)
        self.assertEqual(result['available'], 97)
        self.assertFalse(result['is_at_capacity'])


class CreateCapacityRuleServiceTest(TestCase):
    """Tests for CreateCapacityRuleService."""
    
    def setUp(self):
        self.service = CreateCapacityRuleService()
        
    def test_create_capacity_rule(self):
        """Test creating a capacity rule."""
        data = {
            'event_id': uuid.uuid4(),
            'max_capacity': 100,
            'warning_threshold': 80,
        }
        rule = self.service.execute(data)
        self.assertIsNotNone(rule.id)
        self.assertEqual(rule.max_capacity, 100)
