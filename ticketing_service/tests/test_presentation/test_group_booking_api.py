from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
import uuid

from domain.group_booking import GroupBooking, BulkDiscount


class CreateGroupBookingAPITest(TestCase):
    """Tests for create group booking API."""
    
    def setUp(self):
        self.client = APIClient()
        self.event_id = uuid.uuid4()
    
    def test_create_group_booking(self):
        """Test creating group booking."""
        data = {
            'organizer_id': str(uuid.uuid4()),
            'group_name': 'Tech Conference Group',
            'min_participants': 5,
            'max_participants': 10
        }
        
        response = self.client.post(
            f'/api/tickets/events/{self.event_id}/group-booking/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['group_name'], 'Tech Conference Group')
        self.assertEqual(response.data['status'], 'pending')


class JoinGroupBookingAPITest(TestCase):
    """Tests for join group booking API."""
    
    def setUp(self):
        self.client = APIClient()
        self.booking = GroupBooking.objects.create(
            event_id=uuid.uuid4(),
            organizer_id=uuid.uuid4(),
            group_name='Test Group',
            min_participants=3,
            max_participants=5
        )
    
    def test_join_group_booking(self):
        """Test joining group booking."""
        data = {'user_id': str(uuid.uuid4())}
        
        response = self.client.post(
            f'/api/tickets/group-bookings/{self.booking.id}/join/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['current_participants'], 1)


class ProcessGroupPaymentAPITest(TestCase):
    """Tests for process group payment API."""
    
    def setUp(self):
        self.client = APIClient()
        self.event_id = uuid.uuid4()
        self.booking = GroupBooking.objects.create(
            event_id=self.event_id,
            organizer_id=uuid.uuid4(),
            group_name='Payment Group',
            min_participants=5,
            max_participants=10,
            current_participants=5
        )
        BulkDiscount.objects.create(
            event_id=self.event_id,
            min_quantity=5,
            discount_type='percentage',
            discount_value=Decimal('20.00')
        )
    
    def test_process_group_payment(self):
        """Test processing group payment."""
        data = {'base_price': '100.00'}
        
        response = self.client.post(
            f'/api/tickets/group-bookings/{self.booking.id}/payment/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['quantity'], 5)
        self.assertEqual(response.data['final_total'], '400.00')
