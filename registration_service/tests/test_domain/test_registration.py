import uuid
from django.test import TestCase
from django.core.exceptions import ValidationError

from domain.registration import Registration


class RegistrationModelTest(TestCase):
    """Tests for Registration domain model."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        
    def test_create_registration(self):
        """Test creating a valid registration."""
        registration = Registration.objects.create(
            event_id=self.event_id,
            user_id=self.user_id,
            attendee_name="John Doe",
            attendee_email="john@example.com",
        )
        self.assertIsNotNone(registration.id)
        self.assertEqual(registration.status, 'confirmed')
        self.assertTrue(registration.is_active())
        
    def test_unique_registration(self):
        """Test user can only register once per event."""
        Registration.objects.create(
            event_id=self.event_id,
            user_id=self.user_id,
            attendee_name="John Doe",
            attendee_email="john@example.com",
        )
        with self.assertRaises(Exception):
            Registration.objects.create(
                event_id=self.event_id,
                user_id=self.user_id,
                attendee_name="John Doe",
                attendee_email="john@example.com",
            )
            
    def test_cancel_registration(self):
        """Test cancelling a registration."""
        registration = Registration.objects.create(
            event_id=self.event_id,
            user_id=self.user_id,
            attendee_name="John Doe",
            attendee_email="john@example.com",
        )
        registration.cancel()
        self.assertEqual(registration.status, 'cancelled')
        self.assertIsNotNone(registration.cancelled_at)
        self.assertFalse(registration.is_active())
        
    def test_cannot_cancel_twice(self):
        """Test cannot cancel already cancelled registration."""
        registration = Registration.objects.create(
            event_id=self.event_id,
            user_id=self.user_id,
            attendee_name="John Doe",
            attendee_email="john@example.com",
        )
        registration.cancel()
        with self.assertRaises(ValidationError):
            registration.cancel()
            
    def test_confirm_waitlisted(self):
        """Test confirming a waitlisted registration."""
        registration = Registration.objects.create(
            event_id=self.event_id,
            user_id=self.user_id,
            attendee_name="John Doe",
            attendee_email="john@example.com",
            status='waitlisted',
        )
        registration.confirm()
        self.assertEqual(registration.status, 'confirmed')
        
    def test_cannot_confirm_non_waitlisted(self):
        """Test cannot confirm non-waitlisted registration."""
        registration = Registration.objects.create(
            event_id=self.event_id,
            user_id=self.user_id,
            attendee_name="John Doe",
            attendee_email="john@example.com",
            status='confirmed',
        )
        with self.assertRaises(ValidationError):
            registration.confirm()
