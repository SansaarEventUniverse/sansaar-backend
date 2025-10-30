import uuid
import json
from decimal import Decimal
from django.test import TestCase, Client

from domain.group_registration import GroupRegistration


class GroupAPITest(TestCase):
    """Tests for Group API endpoints."""
    
    def setUp(self):
        self.client = Client()
        self.event_id = uuid.uuid4()
        
    def test_create_group(self):
        """Test creating group via API."""
        data = {
            'group_name': 'Tech Team',
            'group_leader_id': str(uuid.uuid4()),
            'group_leader_email': 'leader@example.com',
            'max_size': 10,
            'price_per_person': '50.00',
        }
        response = self.client.post(
            f'/api/registrations/events/{self.event_id}/groups/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['group_name'], 'Tech Team')
        
    def test_join_group(self):
        """Test joining group via API."""
        group = GroupRegistration.objects.create(
            event_id=self.event_id,
            group_name='Test Group',
            group_leader_id=uuid.uuid4(),
            group_leader_email='leader@example.com',
            max_size=10,
        )
        
        data = {
            'user_id': str(uuid.uuid4()),
            'name': 'John Doe',
            'email': 'john@example.com',
        }
        response = self.client.post(
            f'/api/registrations/events/{self.event_id}/groups/{group.id}/join/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        group.refresh_from_db()
        self.assertEqual(group.current_size, 1)
        
    def test_get_group(self):
        """Test getting group via API."""
        group = GroupRegistration.objects.create(
            event_id=self.event_id,
            group_name='Test Group',
            group_leader_id=uuid.uuid4(),
            group_leader_email='leader@example.com',
            max_size=10,
        )
        
        response = self.client.get(
            f'/api/registrations/events/{self.event_id}/groups/{group.id}/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['group_name'], 'Test Group')
        
    def test_confirm_group(self):
        """Test confirming group via API."""
        group = GroupRegistration.objects.create(
            event_id=self.event_id,
            group_name='Test Group',
            group_leader_id=uuid.uuid4(),
            group_leader_email='leader@example.com',
            min_size=2,
            max_size=10,
            current_size=3,
        )
        
        response = self.client.post(
            f'/api/registrations/events/{self.event_id}/groups/{group.id}/confirm/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'confirmed')
        
    def test_get_group_stats(self):
        """Test getting group stats via API."""
        GroupRegistration.objects.create(
            event_id=self.event_id,
            group_name='Group 1',
            group_leader_id=uuid.uuid4(),
            group_leader_email='leader1@example.com',
            max_size=10,
            current_size=5,
        )
        
        response = self.client.get(
            f'/api/registrations/events/{self.event_id}/groups/stats/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total_groups'], 1)
        self.assertEqual(response.json()['total_members'], 5)
