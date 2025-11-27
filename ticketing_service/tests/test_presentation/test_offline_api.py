from datetime import timedelta
from django.test import TestCase
from rest_framework.test import APIClient
from django.utils import timezone
import uuid

from domain.offline import OfflineTicket, ValidationCache


class ValidateOfflineAPITest(TestCase):
    """Tests for offline validation API."""
    
    def setUp(self):
        self.client = APIClient()
        self.ticket = OfflineTicket.objects.create(
            ticket_id=uuid.uuid4(),
            qr_code='QR123',
            event_id=uuid.uuid4(),
            attendee_name='John Doe',
            valid_until=timezone.now() + timedelta(days=1)
        )
    
    def test_validate_offline(self):
        """Test validating ticket offline."""
        data = {'qr_code': 'QR123'}
        
        response = self.client.post('/api/tickets/validate-offline/', data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'validated')


class SyncTicketDataAPITest(TestCase):
    """Tests for ticket sync API."""
    
    def setUp(self):
        self.client = APIClient()
        self.event_id = uuid.uuid4()
    
    def test_sync_tickets(self):
        """Test syncing tickets."""
        data = {
            'event_id': str(self.event_id),
            'tickets': [
                {
                    'ticket_id': str(uuid.uuid4()),
                    'qr_code': 'QR001',
                    'attendee_name': 'Alice',
                    'valid_until': (timezone.now() + timedelta(days=1)).isoformat()
                }
            ]
        }
        
        response = self.client.post('/api/tickets/sync/', data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['synced_count'], 1)


class OfflineStatusAPITest(TestCase):
    """Tests for offline status API."""
    
    def setUp(self):
        self.client = APIClient()
        self.event_id = uuid.uuid4()
        self.cache = ValidationCache.objects.create(
            event_id=self.event_id,
            cache_data={'tickets': ['t1', 't2']},
            ticket_count=2,
            expires_at=timezone.now() + timedelta(hours=1)
        )
    
    def test_get_offline_status(self):
        """Test getting offline status."""
        response = self.client.get(f'/api/tickets/events/{self.event_id}/offline-status/')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['ticket_count'], 2)
        self.assertEqual(response.data['cache_status'], 'active')
