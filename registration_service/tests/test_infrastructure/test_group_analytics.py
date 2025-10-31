import uuid
from django.test import TestCase

from domain.group_registration import GroupRegistration
from infrastructure.services.group_analytics_service import GroupAnalyticsService


class GroupAnalyticsServiceTest(TestCase):
    """Tests for GroupAnalyticsService."""
    
    def test_get_group_stats(self):
        """Test getting group statistics."""
        event_id = uuid.uuid4()
        
        GroupRegistration.objects.create(
            event_id=event_id,
            group_name='Group 1',
            group_leader_id=uuid.uuid4(),
            group_leader_email='leader1@example.com',
            max_size=10,
            current_size=5,
            status='confirmed',
        )
        
        GroupRegistration.objects.create(
            event_id=event_id,
            group_name='Group 2',
            group_leader_id=uuid.uuid4(),
            group_leader_email='leader2@example.com',
            max_size=8,
            current_size=3,
        )
        
        service = GroupAnalyticsService()
        stats = service.get_group_stats(event_id)
        
        self.assertEqual(stats['total_groups'], 2)
        self.assertEqual(stats['confirmed_groups'], 1)
        self.assertEqual(stats['total_members'], 8)
        self.assertEqual(stats['average_group_size'], 4.0)
