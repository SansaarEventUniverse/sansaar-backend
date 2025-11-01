import uuid
from django.test import TestCase

from domain.registration import Registration
from domain.waitlist import Waitlist
from domain.capacity_rule import CapacityRule
from application.registration_service import RegisterForEventService
from application.waitlist_service import JoinWaitlistService, ProcessWaitlistService
from infrastructure.services.capacity_tracking_service import CapacityTrackingService


class WaitlistIntegrationTest(TestCase):
    """Integration tests for waitlist processing."""
    
    def test_full_waitlist_workflow(self):
        """Test complete waitlist workflow with promotion."""
        event_id = uuid.uuid4()
        
        # Create capacity rule
        CapacityRule.objects.create(
            event_id=event_id,
            max_capacity=2,
            warning_threshold=80,
        )
        
        # Register 2 users (fill capacity)
        register_service = RegisterForEventService()
        register_service.execute({
            'event_id': str(event_id),
            'user_id': str(uuid.uuid4()),
            'attendee_name': 'User 1',
            'attendee_email': 'user1@example.com',
        })
        register_service.execute({
            'event_id': str(event_id),
            'user_id': str(uuid.uuid4()),
            'attendee_name': 'User 2',
            'attendee_email': 'user2@example.com',
        })
        
        # Join waitlist
        waitlist_service = JoinWaitlistService()
        user3_id = uuid.uuid4()
        waitlist_entry = waitlist_service.execute({
            'event_id': str(event_id),
            'user_id': str(user3_id),
        })
        
        self.assertEqual(waitlist_entry.position, 1)
        self.assertFalse(waitlist_entry.is_promoted)
        
        # Cancel one registration
        registration = Registration.objects.filter(event_id=event_id).first()
        registration.status = 'cancelled'
        registration.save()
        
        # Promote from waitlist
        promote_service = ProcessWaitlistService()
        promoted = promote_service.execute(event_id, 1)
        
        self.assertEqual(len(promoted), 1)
        self.assertEqual(promoted[0].user_id, user3_id)
        self.assertTrue(promoted[0].is_promoted)


class CapacityTrackingIntegrationTest(TestCase):
    """Integration tests for capacity tracking."""
    
    def test_real_time_capacity_updates(self):
        """Test real-time capacity tracking with Redis."""
        event_id = uuid.uuid4()
        capacity_service = CapacityTrackingService()
        
        # Initial state
        self.assertEqual(capacity_service.get_registered_count(event_id), 0)
        
        # Increment capacity
        capacity_service.increment_capacity(event_id)
        capacity_service.increment_capacity(event_id)
        
        self.assertEqual(capacity_service.get_registered_count(event_id), 2)
        
        # Check capacity with limit
        CapacityRule.objects.create(
            event_id=event_id,
            max_capacity=5,
            warning_threshold=80,
        )
        
        available = capacity_service.check_capacity(event_id, 5)
        self.assertTrue(available)
        
        # Fill to capacity
        capacity_service.increment_capacity(event_id)
        capacity_service.increment_capacity(event_id)
        capacity_service.increment_capacity(event_id)
        
        available = capacity_service.check_capacity(event_id, 5)
        self.assertFalse(available)


class RegistrationWorkflowTest(TestCase):
    """End-to-end tests for registration workflows."""
    
    def test_complete_registration_workflow(self):
        """Test complete registration workflow from start to finish."""
        event_id = uuid.uuid4()
        user_id = uuid.uuid4()
        
        # Step 1: Create capacity rule
        CapacityRule.objects.create(
            event_id=event_id,
            max_capacity=10,
            warning_threshold=80,
        )
        
        # Step 2: Register for event
        register_service = RegisterForEventService()
        registration = register_service.execute({
            'event_id': str(event_id),
            'user_id': str(user_id),
            'attendee_name': 'Test User',
            'attendee_email': 'test@example.com',
        })
        
        self.assertEqual(registration.status, 'confirmed')
        
        # Step 3: Verify registration exists
        self.assertTrue(
            Registration.objects.filter(
                event_id=event_id,
                user_id=user_id,
                status='confirmed'
            ).exists()
        )
        
        # Step 4: Cancel registration
        registration.status = 'cancelled'
        registration.save()
        
        # Verify registration cancelled
        registration.refresh_from_db()
        self.assertEqual(registration.status, 'cancelled')
