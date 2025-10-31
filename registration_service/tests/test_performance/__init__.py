import uuid
import time
from django.test import TestCase
from concurrent.futures import ThreadPoolExecutor

from domain.registration import Registration
from domain.group_registration import GroupRegistration, GroupMember
from application.group_service import AddGroupMemberService
from application.analytics_service import GenerateAnalyticsService
from infrastructure.services.capacity_tracking_service import CapacityTrackingService


class CapacityPerformanceTest(TestCase):
    """Performance tests for capacity tracking."""
    
    def test_concurrent_capacity_updates(self):
        """Test capacity tracking under concurrent load."""
        event_id = uuid.uuid4()
        capacity_service = CapacityTrackingService()
        
        def increment():
            capacity_service.increment_capacity(event_id)
        
        # Simulate 50 concurrent registrations
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(increment) for _ in range(50)]
            for future in futures:
                future.result()
        
        # Verify count is accurate
        count = capacity_service.get_registered_count(event_id)
        self.assertEqual(count, 50)
    
    def test_capacity_check_performance(self):
        """Test capacity check performance."""
        event_id = uuid.uuid4()
        capacity_service = CapacityTrackingService()
        
        # Warm up
        capacity_service.check_capacity(event_id, 100)
        
        # Measure performance
        start = time.time()
        for _ in range(1000):
            capacity_service.check_capacity(event_id, 100)
        duration = time.time() - start
        
        # Should complete 1000 checks in under 1 second
        self.assertLess(duration, 1.0)


class GroupCoordinationPerformanceTest(TestCase):
    """Performance tests for group coordination."""
    
    def test_add_multiple_members_performance(self):
        """Test adding multiple members to group."""
        event_id = uuid.uuid4()
        group = GroupRegistration.objects.create(
            event_id=event_id,
            group_name='Large Group',
            group_leader_id=uuid.uuid4(),
            group_leader_email='leader@example.com',
            max_size=100,
        )
        
        service = AddGroupMemberService()
        
        start = time.time()
        for i in range(50):
            service.execute(
                group.id,
                uuid.uuid4(),
                f'Member {i}',
                f'member{i}@example.com'
            )
        duration = time.time() - start
        
        # Should add 50 members in under 2 seconds
        self.assertLess(duration, 2.0)
        
        group.refresh_from_db()
        self.assertEqual(group.current_size, 50)


class AnalyticsPerformanceTest(TestCase):
    """Performance tests for analytics processing."""
    
    def test_analytics_generation_performance(self):
        """Test analytics generation with large dataset."""
        event_id = uuid.uuid4()
        
        # Create 100 registrations
        for i in range(100):
            Registration.objects.create(
                event_id=event_id,
                user_id=uuid.uuid4(),
                status='confirmed',
                attendee_name=f'User {i}',
                attendee_email=f'user{i}@example.com',
            )
        
        service = GenerateAnalyticsService()
        
        start = time.time()
        analytics = service.execute(event_id)
        duration = time.time() - start
        
        # Should generate analytics in under 0.5 seconds
        self.assertLess(duration, 0.5)
        self.assertEqual(analytics.total_registrations, 100)
