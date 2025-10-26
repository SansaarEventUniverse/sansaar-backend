import uuid
from django.test import TestCase
from django.core.exceptions import ValidationError

from domain.waitlist import Waitlist


class WaitlistModelTest(TestCase):
    """Tests for Waitlist domain model."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        
    def test_create_waitlist(self):
        """Test creating a waitlist entry."""
        waitlist = Waitlist.objects.create(
            event_id=self.event_id,
            user_id=self.user_id,
            position=1,
        )
        self.assertIsNotNone(waitlist.id)
        self.assertEqual(waitlist.position, 1)
        self.assertFalse(waitlist.is_promoted)
        
    def test_unique_waitlist(self):
        """Test user can only be on waitlist once per event."""
        Waitlist.objects.create(
            event_id=self.event_id,
            user_id=self.user_id,
            position=1,
        )
        with self.assertRaises(Exception):
            Waitlist.objects.create(
                event_id=self.event_id,
                user_id=self.user_id,
                position=2,
            )
            
    def test_promote_from_waitlist(self):
        """Test promoting from waitlist."""
        waitlist = Waitlist.objects.create(
            event_id=self.event_id,
            user_id=self.user_id,
            position=1,
        )
        waitlist.promote()
        self.assertTrue(waitlist.is_promoted)
        self.assertIsNotNone(waitlist.promoted_at)
        
    def test_cannot_promote_twice(self):
        """Test cannot promote twice."""
        waitlist = Waitlist.objects.create(
            event_id=self.event_id,
            user_id=self.user_id,
            position=1,
        )
        waitlist.promote()
        with self.assertRaises(ValidationError):
            waitlist.promote()
            
    def test_update_position(self):
        """Test updating waitlist position."""
        waitlist = Waitlist.objects.create(
            event_id=self.event_id,
            user_id=self.user_id,
            position=5,
        )
        waitlist.update_position(3)
        self.assertEqual(waitlist.position, 3)
        
    def test_invalid_position(self):
        """Test invalid position."""
        waitlist = Waitlist.objects.create(
            event_id=self.event_id,
            user_id=self.user_id,
            position=1,
        )
        with self.assertRaises(ValidationError):
            waitlist.update_position(0)
