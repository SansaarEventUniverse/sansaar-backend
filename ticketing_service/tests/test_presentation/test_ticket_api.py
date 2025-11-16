from django.test import TestCase
import uuid
import json

from domain.ticket import Ticket


class TicketAPITest(TestCase):
    """Tests for ticket API endpoints."""
    
    def setUp(self):
        self.ticket = Ticket.objects.create(
            ticket_type_id=uuid.uuid4(),
            order_id=uuid.uuid4(),
            attendee_name='John Doe',
            attendee_email='john@example.com'
        )
    
    def test_validate_qr_code(self):
        """Test QR code validation endpoint."""
        data = {'qr_code_data': self.ticket.qr_code_data}
        response = self.client.post(
            '/api/tickets/tickets/validate/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['valid'])
    
    def test_validate_invalid_qr_code(self):
        """Test validating invalid QR code."""
        data = {'qr_code_data': 'invalid_qr'}
        response = self.client.post(
            '/api/tickets/tickets/validate/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_check_in_ticket(self):
        """Test ticket check-in endpoint."""
        data = {'checked_in_by': str(uuid.uuid4())}
        response = self.client.post(
            f'/api/tickets/tickets/{self.ticket.id}/checkin/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'used')
    
    def test_get_ticket(self):
        """Test getting ticket details."""
        response = self.client.get(f'/api/tickets/tickets/{self.ticket.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['attendee_name'], 'John Doe')
    
    def test_get_nonexistent_ticket(self):
        """Test getting non-existent ticket."""
        response = self.client.get(f'/api/tickets/tickets/{uuid.uuid4()}/')
        self.assertEqual(response.status_code, 404)
