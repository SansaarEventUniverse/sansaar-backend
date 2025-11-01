import uuid
import json
from django.test import TestCase, Client

from domain.registration import Registration
from domain.waitlist import Waitlist
from domain.group_registration import GroupRegistration
from domain.capacity_rule import CapacityRule


class RegistrationEndToEndTest(TestCase):
    """End-to-end tests for complete registration workflows."""
    
    def setUp(self):
        self.client = Client()
        self.event_id = uuid.uuid4()
    
    def test_full_registration_flow(self):
        """Test complete registration flow with all features."""
        # Step 1: Create capacity rule
        response = self.client.post(
            f'/api/registrations/events/{self.event_id}/capacity/rule/',
            data=json.dumps({'max_capacity': 5, 'warning_threshold': 80}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        
        # Step 2: Register 3 users
        for i in range(3):
            response = self.client.post(
                f'/api/registrations/events/{self.event_id}/register/',
                data=json.dumps({
                    'user_id': str(uuid.uuid4()),
                    'attendee_name': f'User {i}',
                    'attendee_email': f'user{i}@example.com'
                }),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 201)
        
        # Step 3: Check capacity
        response = self.client.get(
            f'/api/registrations/events/{self.event_id}/capacity/info/'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['confirmed_count'], 3)
        self.assertEqual(data['available'], 2)
        
        # Step 4: Get analytics
        response = self.client.get(
            f'/api/registrations/events/{self.event_id}/analytics/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total_registrations'], 3)
    
    def test_waitlist_to_registration_flow(self):
        """Test waitlist promotion flow."""
        # Create capacity rule (max 2)
        CapacityRule.objects.create(
            event_id=self.event_id,
            max_capacity=2,
            warning_threshold=80,
        )
        
        # Register 2 users (fill capacity)
        for i in range(2):
            self.client.post(
                f'/api/registrations/events/{self.event_id}/register/',
                data=json.dumps({
                    'user_id': str(uuid.uuid4()),
                    'attendee_name': f'User {i}',
                    'attendee_email': f'user{i}@example.com'
                }),
                content_type='application/json'
            )
        
        # Join waitlist
        user3_id = str(uuid.uuid4())
        response = self.client.post(
            f'/api/registrations/events/{self.event_id}/waitlist/',
            data=json.dumps({'user_id': user3_id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        
        # Check waitlist position
        response = self.client.get(
            f'/api/registrations/events/{self.event_id}/waitlist/position/?user_id={user3_id}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['position'], 1)
    
    def test_group_registration_flow(self):
        """Test complete group registration flow."""
        # Create group
        response = self.client.post(
            f'/api/registrations/events/{self.event_id}/groups/',
            data=json.dumps({
                'group_name': 'Test Team',
                'group_leader_id': str(uuid.uuid4()),
                'group_leader_email': 'leader@example.com',
                'max_size': 5,
                'price_per_person': '50.00'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        group_id = response.json()['id']
        
        # Add members
        for i in range(3):
            response = self.client.post(
                f'/api/registrations/events/{self.event_id}/groups/{group_id}/join/',
                data=json.dumps({
                    'user_id': str(uuid.uuid4()),
                    'name': f'Member {i}',
                    'email': f'member{i}@example.com'
                }),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 201)
        
        # Confirm group
        response = self.client.post(
            f'/api/registrations/events/{self.event_id}/groups/{group_id}/confirm/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'confirmed')
        self.assertEqual(response.json()['current_size'], 3)
        
        # Check group stats
        response = self.client.get(
            f'/api/registrations/events/{self.event_id}/groups/stats/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total_groups'], 1)
        self.assertEqual(response.json()['total_members'], 3)
