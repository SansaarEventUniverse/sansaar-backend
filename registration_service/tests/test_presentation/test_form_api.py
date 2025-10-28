import uuid
import json
from django.test import TestCase, Client

from domain.registration_form import RegistrationForm


class FormAPITest(TestCase):
    """Tests for Form API endpoints."""
    
    def setUp(self):
        self.client = Client()
        self.event_id = uuid.uuid4()
        
    def test_create_form(self):
        """Test creating form via API."""
        data = {
            'title': 'Event Registration',
            'fields': [
                {'label': 'Full Name', 'field_type': 'text', 'is_required': True, 'order': 1},
                {'label': 'Email', 'field_type': 'email', 'is_required': True, 'order': 2},
            ]
        }
        response = self.client.post(
            f'/api/registrations/events/{self.event_id}/form/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.json()['fields']), 2)
        
    def test_get_form(self):
        """Test getting form via API."""
        form = RegistrationForm.objects.create(
            event_id=self.event_id,
            title='Registration',
        )
        response = self.client.get(
            f'/api/registrations/events/{self.event_id}/form/get/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Registration')
        
    def test_submit_form(self):
        """Test submitting form via API."""
        form = RegistrationForm.objects.create(
            event_id=self.event_id,
            title='Registration',
        )
        from domain.registration_form import CustomField
        CustomField.objects.create(
            form=form,
            label='Full Name',
            field_type='text',
            is_required=True,
            order=1,
        )
        
        data = {
            'data': {'Full Name': 'John Doe'}
        }
        response = self.client.post(
            f'/api/registrations/events/{self.event_id}/form/submit/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn('submission_id', response.json())
