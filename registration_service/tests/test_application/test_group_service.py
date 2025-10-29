import uuid
from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError

from domain.group_registration import GroupRegistration
from application.group_service import (
    CreateGroupRegistrationService,
    AddGroupMemberService,
    ConfirmGroupRegistrationService,
    CancelGroupRegistrationService,
)


class CreateGroupRegistrationServiceTest(TestCase):
    """Tests for CreateGroupRegistrationService."""
    
    def test_create_group(self):
        """Test creating group registration."""
        service = CreateGroupRegistrationService()
        data = {
            'event_id': str(uuid.uuid4()),
            'group_name': 'Tech Team',
            'group_leader_id': str(uuid.uuid4()),
            'group_leader_email': 'leader@example.com',
            'max_size': 10,
            'price_per_person': '50.00',
        }
        group = service.execute(data)
        self.assertIsNotNone(group.id)
        self.assertEqual(group.group_name, 'Tech Team')


class AddGroupMemberServiceTest(TestCase):
    """Tests for AddGroupMemberService."""
    
    def setUp(self):
        self.group = GroupRegistration.objects.create(
            event_id=uuid.uuid4(),
            group_name='Test Group',
            group_leader_id=uuid.uuid4(),
            group_leader_email='leader@example.com',
            max_size=5,
        )
        
    def test_add_member(self):
        """Test adding member to group."""
        service = AddGroupMemberService()
        member = service.execute(
            self.group.id,
            uuid.uuid4(),
            'John Doe',
            'john@example.com'
        )
        self.assertIsNotNone(member.id)
        self.group.refresh_from_db()
        self.assertEqual(self.group.current_size, 1)
        
    def test_cannot_add_to_full_group(self):
        """Test cannot add to full group."""
        self.group.current_size = 5
        self.group.save()
        
        service = AddGroupMemberService()
        with self.assertRaises(ValidationError):
            service.execute(
                self.group.id,
                uuid.uuid4(),
                'John Doe',
                'john@example.com'
            )


class ConfirmGroupRegistrationServiceTest(TestCase):
    """Tests for ConfirmGroupRegistrationService."""
    
    def test_confirm_group(self):
        """Test confirming group registration."""
        group = GroupRegistration.objects.create(
            event_id=uuid.uuid4(),
            group_name='Test Group',
            group_leader_id=uuid.uuid4(),
            group_leader_email='leader@example.com',
            min_size=2,
            max_size=5,
            current_size=3,
        )
        
        service = ConfirmGroupRegistrationService()
        confirmed = service.execute(group.id)
        self.assertEqual(confirmed.status, 'confirmed')


class CancelGroupRegistrationServiceTest(TestCase):
    """Tests for CancelGroupRegistrationService."""
    
    def test_cancel_group(self):
        """Test cancelling group registration."""
        group = GroupRegistration.objects.create(
            event_id=uuid.uuid4(),
            group_name='Test Group',
            group_leader_id=uuid.uuid4(),
            group_leader_email='leader@example.com',
            max_size=5,
        )
        
        service = CancelGroupRegistrationService()
        cancelled = service.execute(group.id)
        self.assertEqual(cancelled.status, 'cancelled')
        self.assertIsNotNone(cancelled.cancelled_at)
