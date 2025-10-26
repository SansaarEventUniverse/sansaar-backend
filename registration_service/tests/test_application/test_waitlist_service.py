import uuid
from django.test import TestCase
from django.core.exceptions import ValidationError

from application.waitlist_service import (
    JoinWaitlistService,
    LeaveWaitlistService,
    ProcessWaitlistService,
    GetWaitlistPositionService,
)
from domain.waitlist import Waitlist


class JoinWaitlistServiceTest(TestCase):
    """Tests for JoinWaitlistService."""
    
    def setUp(self):
        self.service = JoinWaitlistService()
        self.event_id = uuid.uuid4()
        
    def test_join_waitlist(self):
        """Test joining waitlist."""
        data = {
            'event_id': self.event_id,
            'user_id': uuid.uuid4(),
        }
        waitlist = self.service.execute(data)
        self.assertEqual(waitlist.position, 1)
        
    def test_join_waitlist_position(self):
        """Test waitlist position increments."""
        self.service.execute({'event_id': self.event_id, 'user_id': uuid.uuid4()})
        waitlist2 = self.service.execute({'event_id': self.event_id, 'user_id': uuid.uuid4()})
        self.assertEqual(waitlist2.position, 2)


class ProcessWaitlistServiceTest(TestCase):
    """Tests for ProcessWaitlistService."""
    
    def setUp(self):
        self.service = ProcessWaitlistService()
        self.event_id = uuid.uuid4()
        
    def test_process_waitlist(self):
        """Test processing waitlist."""
        # Create waitlist entries
        for i in range(3):
            Waitlist.objects.create(
                event_id=self.event_id,
                user_id=uuid.uuid4(),
                position=i+1,
            )
        
        promoted = self.service.execute(self.event_id, available_spots=2)
        self.assertEqual(len(promoted), 2)
        self.assertTrue(all(w.is_promoted for w in promoted))


class GetWaitlistPositionServiceTest(TestCase):
    """Tests for GetWaitlistPositionService."""
    
    def setUp(self):
        self.service = GetWaitlistPositionService()
        self.event_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        
    def test_get_position(self):
        """Test getting waitlist position."""
        Waitlist.objects.create(
            event_id=self.event_id,
            user_id=uuid.uuid4(),
            position=1,
        )
        Waitlist.objects.create(
            event_id=self.event_id,
            user_id=self.user_id,
            position=2,
        )
        
        result = self.service.execute(self.event_id, self.user_id)
        self.assertEqual(result['position'], 2)
        self.assertEqual(result['users_ahead'], 1)
