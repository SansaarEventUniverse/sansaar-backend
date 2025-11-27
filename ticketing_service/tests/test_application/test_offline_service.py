from datetime import timedelta
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid

from domain.offline import OfflineTicket, ValidationCache
from application.offline_service import (
    OfflineValidationService,
    TicketSyncService,
    CacheManagementService
)


class OfflineValidationServiceTest(TestCase):
    """Tests for OfflineValidationService."""
    
    def setUp(self):
        self.service = OfflineValidationService()
        self.ticket = OfflineTicket.objects.create(
            ticket_id=uuid.uuid4(),
            qr_code='QR123',
            event_id=uuid.uuid4(),
            attendee_name='John Doe',
            valid_until=timezone.now() + timedelta(days=1)
        )
    
    def test_validate_ticket(self):
        """Test validating ticket offline."""
        result = self.service.validate_ticket('QR123')
        
        self.assertEqual(result['status'], 'validated')
        self.assertEqual(result['attendee_name'], 'John Doe')
        
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, 'used')
    
    def test_validate_nonexistent_ticket(self):
        """Test validating non-existent ticket."""
        with self.assertRaises(ValidationError):
            self.service.validate_ticket('INVALID')


class TicketSyncServiceTest(TestCase):
    """Tests for TicketSyncService."""
    
    def setUp(self):
        self.service = TicketSyncService()
        self.event_id = uuid.uuid4()
    
    def test_sync_tickets(self):
        """Test syncing tickets."""
        tickets = [
            {
                'ticket_id': uuid.uuid4(),
                'qr_code': 'QR001',
                'attendee_name': 'Alice',
                'valid_until': timezone.now() + timedelta(days=1)
            },
            {
                'ticket_id': uuid.uuid4(),
                'qr_code': 'QR002',
                'attendee_name': 'Bob',
                'valid_until': timezone.now() + timedelta(days=1)
            }
        ]
        
        result = self.service.sync_tickets(self.event_id, tickets)
        
        self.assertEqual(result['synced_count'], 2)
        self.assertEqual(OfflineTicket.objects.filter(event_id=self.event_id).count(), 2)


class CacheManagementServiceTest(TestCase):
    """Tests for CacheManagementService."""
    
    def setUp(self):
        self.service = CacheManagementService()
        self.event_id = uuid.uuid4()
    
    def test_create_cache(self):
        """Test creating cache."""
        data = {'tickets': ['t1', 't2']}
        
        cache = self.service.create_cache(self.event_id, data)
        
        self.assertEqual(cache.ticket_count, 2)
        self.assertFalse(cache.is_expired())
    
    def test_get_cache(self):
        """Test getting cache."""
        data = {'tickets': ['t1']}
        self.service.create_cache(self.event_id, data)
        
        cache = self.service.get_cache(self.event_id)
        
        self.assertEqual(cache.ticket_count, 1)
