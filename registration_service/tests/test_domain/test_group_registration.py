import uuid
from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError

from domain.group_registration import GroupRegistration, GroupMember


class GroupRegistrationModelTest(TestCase):
    """Tests for GroupRegistration model."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
        self.leader_id = uuid.uuid4()
        
    def test_create_group(self):
        """Test creating a group registration."""
        group = GroupRegistration.objects.create(
            event_id=self.event_id,
            group_name='Tech Team',
            group_leader_id=self.leader_id,
            group_leader_email='leader@example.com',
            max_size=10,
            price_per_person=Decimal('50.00'),
        )
        self.assertIsNotNone(group.id)
        self.assertEqual(group.status, 'pending')
        
    def test_min_size_validation(self):
        """Test minimum size validation."""
        group = GroupRegistration(
            event_id=self.event_id,
            group_name='Small Group',
            group_leader_id=self.leader_id,
            group_leader_email='leader@example.com',
            min_size=1,
            max_size=5,
        )
        with self.assertRaises(ValidationError):
            group.clean()
            
    def test_is_full(self):
        """Test group full check."""
        group = GroupRegistration.objects.create(
            event_id=self.event_id,
            group_name='Full Group',
            group_leader_id=self.leader_id,
            group_leader_email='leader@example.com',
            max_size=5,
            current_size=5,
        )
        self.assertTrue(group.is_full())
        
    def test_calculate_total(self):
        """Test total calculation."""
        group = GroupRegistration.objects.create(
            event_id=self.event_id,
            group_name='Paid Group',
            group_leader_id=self.leader_id,
            group_leader_email='leader@example.com',
            max_size=10,
            current_size=5,
            price_per_person=Decimal('50.00'),
        )
        group.calculate_total()
        self.assertEqual(group.total_amount, Decimal('250.00'))


class GroupMemberModelTest(TestCase):
    """Tests for GroupMember model."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
        self.leader_id = uuid.uuid4()
        self.group = GroupRegistration.objects.create(
            event_id=self.event_id,
            group_name='Test Group',
            group_leader_id=self.leader_id,
            group_leader_email='leader@example.com',
            max_size=10,
        )
        
    def test_add_member(self):
        """Test adding a member to group."""
        member = GroupMember.objects.create(
            group=self.group,
            user_id=uuid.uuid4(),
            name='John Doe',
            email='john@example.com',
        )
        self.assertIsNotNone(member.id)
        self.assertEqual(self.group.members.count(), 1)
