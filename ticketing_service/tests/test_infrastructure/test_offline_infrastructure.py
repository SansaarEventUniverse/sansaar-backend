from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
import uuid

from domain.offline import OfflineTicket
from infrastructure.offline_engine import (
    OfflineValidationEngine,
    TicketDataSync,
    OfflineAnalytics,
    ConflictResolution
)


class OfflineValidationEngineTest(TestCase):
    """Tests for OfflineValidationEngine."""
    
    def setUp(self):
        self.engine = OfflineValidationEngine()
        self.ticket = OfflineTicket.objects.create(
            ticket_id=uuid.uuid4(),
            qr_code='QR123',
            event_id=uuid.uuid4(),
            attendee_name='John Doe',
            valid_until=timezone.now() + timedelta(days=1)
        )
    
    def test_validate_valid_ticket(self):
        """Test validating valid ticket."""
        result = self.engine.validate('QR123')
        
        self.assertTrue(result['valid'])
        self.assertEqual(result['attendee_name'], 'John Doe')
    
    def test_validate_nonexistent_ticket(self):
        """Test validating non-existent ticket."""
        result = self.engine.validate('INVALID')
        
        self.assertFalse(result['valid'])
        self.assertEqual(result['reason'], 'Ticket not found')


class TicketDataSyncTest(TestCase):
    """Tests for TicketDataSync."""
    
    def setUp(self):
        self.sync = TicketDataSync()
        self.event_id = uuid.uuid4()
    
    def test_sync_from_server(self):
        """Test syncing from server."""
        tickets = [
            {
                'ticket_id': uuid.uuid4(),
                'qr_code': 'QR001',
                'attendee_name': 'Alice',
                'valid_until': timezone.now() + timedelta(days=1)
            }
        ]
        
        result = self.sync.sync_from_server(self.event_id, tickets)
        
        self.assertEqual(result['synced_count'], 1)
        self.assertEqual(len(result['synced_ids']), 1)


class OfflineAnalyticsTest(TestCase):
    """Tests for OfflineAnalytics."""
    
    def setUp(self):
        self.analytics = OfflineAnalytics()
    
    def test_track_validation(self):
        """Test tracking validation."""
        ticket_id = uuid.uuid4()
        
        result = self.analytics.track_validation(ticket_id)
        
        self.assertEqual(result['mode'], 'offline')
        self.assertIn('validated_at', result)


class ConflictResolutionTest(TestCase):
    """Tests for ConflictResolution."""
    
    def setUp(self):
        self.resolver = ConflictResolution()
        self.ticket = OfflineTicket.objects.create(
            ticket_id=uuid.uuid4(),
            qr_code='QR123',
            event_id=uuid.uuid4(),
            attendee_name='John Doe',
            status='active',
            valid_until=timezone.now() + timedelta(days=1)
        )
    
    def test_resolve_conflict(self):
        """Test resolving conflict."""
        server_data = {
            'status': 'used',
            'valid_until': timezone.now() + timedelta(days=2)
        }
        
        resolved = self.resolver.resolve(self.ticket, server_data)
        
        self.assertEqual(resolved.status, 'used')
