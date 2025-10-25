import uuid
from django.test import TestCase
from django.core.exceptions import ValidationError

from application.registration_service import (
    RegisterForEventService,
    CancelRegistrationService,
    CheckCapacityService,
    GetRegistrationService,
)
from domain.registration import Registration


class RegisterForEventServiceTest(TestCase):
    """Tests for RegisterForEventService."""
    
    def setUp(self):
        self.service = RegisterForEventService()
        self.event_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        
    def test_register_for_event(self):
        """Test registering for an event."""
        data = {
            'event_id': self.event_id,
            'user_id': self.user_id,
            'attendee_name': 'John Doe',
            'attendee_email': 'john@example.com',
        }
        registration = self.service.execute(data)
        self.assertIsNotNone(registration.id)
        self.assertEqual(registration.status, 'confirmed')
        
    def test_duplicate_registration(self):
        """Test cannot register twice."""
        data = {
            'event_id': self.event_id,
            'user_id': self.user_id,
            'attendee_name': 'John Doe',
            'attendee_email': 'john@example.com',
        }
        self.service.execute(data)
        with self.assertRaises(ValidationError):
            self.service.execute(data)


class CancelRegistrationServiceTest(TestCase):
    """Tests for CancelRegistrationService."""
    
    def setUp(self):
        self.service = CancelRegistrationService()
        self.event_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        self.registration = Registration.objects.create(
            event_id=self.event_id,
            user_id=self.user_id,
            attendee_name='John Doe',
            attendee_email='john@example.com',
        )
        
    def test_cancel_registration(self):
        """Test cancelling a registration."""
        result = self.service.execute(self.event_id, self.user_id)
        self.assertEqual(result.status, 'cancelled')


class CheckCapacityServiceTest(TestCase):
    """Tests for CheckCapacityService."""
    
    def setUp(self):
        self.service = CheckCapacityService()
        self.event_id = uuid.uuid4()
        
    def test_check_capacity(self):
        """Test checking event capacity."""
        # Create 2 registrations
        for i in range(2):
            Registration.objects.create(
                event_id=self.event_id,
                user_id=uuid.uuid4(),
                attendee_name=f'User {i}',
                attendee_email=f'user{i}@example.com',
            )
        
        result = self.service.execute(self.event_id, max_capacity=5)
        self.assertEqual(result['confirmed_count'], 2)
        self.assertEqual(result['available'], 3)
        self.assertTrue(result['has_capacity'])


class GetRegistrationServiceTest(TestCase):
    """Tests for GetRegistrationService."""
    
    def setUp(self):
        self.service = GetRegistrationService()
        self.event_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        self.registration = Registration.objects.create(
            event_id=self.event_id,
            user_id=self.user_id,
            attendee_name='John Doe',
            attendee_email='john@example.com',
        )
        
    def test_get_registration(self):
        """Test getting a registration."""
        result = self.service.execute(self.event_id, self.user_id)
        self.assertEqual(result.id, self.registration.id)
