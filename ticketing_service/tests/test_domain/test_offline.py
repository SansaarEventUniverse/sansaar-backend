from datetime import timedelta
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid

from domain.offline import OfflineTicket, ValidationCache


class OfflineTicketModelTest(TestCase):
    """Tests for OfflineTicket model."""
    
    def setUp(self):
        self.ticket_id = uuid.uuid4()
        self.event_id = uuid.uuid4()
        self.valid_until = timezone.now() + timedelta(days=1)
    
    def test_create_offline_ticket(self):
        """Test creating an offline ticket."""
        ticket = OfflineTicket.objects.create(
            ticket_id=self.ticket_id,
            qr_code='QR123',
            event_id=self.event_id,
            attendee_name='John Doe',
            valid_until=self.valid_until
        )
        
        self.assertEqual(ticket.status, 'active')
        self.assertTrue(ticket.is_valid())
    
    def test_validate_offline(self):
        """Test offline validation."""
        ticket = OfflineTicket.objects.create(
            ticket_id=self.ticket_id,
            qr_code='QR456',
            event_id=self.event_id,
            attendee_name='Jane Doe',
            valid_until=self.valid_until
        )
        
        self.assertTrue(ticket.validate_offline())
    
    def test_mark_used(self):
        """Test marking ticket as used."""
        ticket = OfflineTicket.objects.create(
            ticket_id=self.ticket_id,
            qr_code='QR789',
            event_id=self.event_id,
            attendee_name='Bob Smith',
            valid_until=self.valid_until
        )
        
        ticket.mark_used()
        self.assertEqual(ticket.status, 'used')
    
    def test_cannot_use_twice(self):
        """Test cannot use ticket twice."""
        ticket = OfflineTicket.objects.create(
            ticket_id=self.ticket_id,
            qr_code='QR101',
            event_id=self.event_id,
            attendee_name='Alice Brown',
            valid_until=self.valid_until
        )
        
        ticket.mark_used()
        
        with self.assertRaises(ValidationError):
            ticket.mark_used()
    
    def test_expired_ticket(self):
        """Test expired ticket validation."""
        ticket = OfflineTicket.objects.create(
            ticket_id=self.ticket_id,
            qr_code='QR202',
            event_id=self.event_id,
            attendee_name='Charlie Green',
            valid_until=timezone.now() - timedelta(days=1)
        )
        
        self.assertFalse(ticket.is_valid())


class ValidationCacheModelTest(TestCase):
    """Tests for ValidationCache model."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
        self.expires_at = timezone.now() + timedelta(hours=1)
    
    def test_create_cache(self):
        """Test creating validation cache."""
        cache = ValidationCache.objects.create(
            event_id=self.event_id,
            cache_data={'tickets': []},
            expires_at=self.expires_at
        )
        
        self.assertEqual(cache.ticket_count, 0)
        self.assertFalse(cache.is_expired())
    
    def test_update_cache(self):
        """Test updating cache data."""
        cache = ValidationCache.objects.create(
            event_id=self.event_id,
            cache_data={},
            expires_at=self.expires_at
        )
        
        cache.update_cache({'tickets': ['t1', 't2', 't3']})
        self.assertEqual(cache.ticket_count, 3)
    
    def test_expired_cache(self):
        """Test expired cache detection."""
        cache = ValidationCache.objects.create(
            event_id=self.event_id,
            cache_data={},
            expires_at=timezone.now() - timedelta(hours=1)
        )
        
        self.assertTrue(cache.is_expired())
