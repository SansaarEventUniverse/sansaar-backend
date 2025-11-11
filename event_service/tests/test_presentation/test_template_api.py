import uuid
import json
from django.test import TestCase, Client

from domain.template import EventTemplate


class TemplateAPITest(TestCase):
    """Tests for Template API endpoints."""
    
    def setUp(self):
        self.client = Client()
        self.user_id = uuid.uuid4()
        
    def test_create_template(self):
        """Test creating template via API."""
        data = {
            'name': 'Conference Template',
            'description': 'Standard conference template',
            'category': 'conference',
            'template_data': {
                'title': 'Annual Conference',
                'description': 'Conference description',
            },
            'visibility': 'public',
            'created_by': str(self.user_id),
        }
        
        response = self.client.post(
            '/api/events/templates/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        result = response.json()
        self.assertEqual(result['name'], 'Conference Template')
        
    def test_get_templates(self):
        """Test getting templates via API."""
        EventTemplate.objects.create(
            name='Public Template',
            description='Public',
            category='workshop',
            template_data={'title': 'Workshop', 'description': 'Test'},
            created_by=uuid.uuid4(),
            visibility='public',
        )
        
        response = self.client.get(
            f'/api/events/templates/list/?user_id={self.user_id}'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        
    def test_get_template(self):
        """Test getting single template via API."""
        template = EventTemplate.objects.create(
            name='Test Template',
            description='Test',
            category='meetup',
            template_data={'title': 'Meetup', 'description': 'Test'},
            created_by=self.user_id,
        )
        
        response = self.client.get(
            f'/api/events/templates/{template.id}/'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['name'], 'Test Template')
        
    def test_apply_template(self):
        """Test applying template via API."""
        template = EventTemplate.objects.create(
            name='Apply Template',
            description='Test',
            category='webinar',
            template_data={'title': 'Webinar', 'description': 'Test', 'duration': 2},
            created_by=self.user_id,
            visibility='public',
        )
        
        event_id = uuid.uuid4()
        data = {
            'template_id': str(template.id),
            'event_data': {'title': 'My Webinar', 'location': 'Online'},
            'user_id': str(self.user_id),
        }
        
        response = self.client.post(
            f'/api/events/{event_id}/apply-template/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['event_data']['title'], 'My Webinar')
        self.assertEqual(result['event_data']['duration'], 2)
        
    def test_update_template(self):
        """Test updating template via API."""
        template = EventTemplate.objects.create(
            name='Original Name',
            description='Original',
            category='conference',
            template_data={'title': 'Event', 'description': 'Test'},
            created_by=self.user_id,
        )
        
        data = {
            'name': 'Updated Name',
            'user_id': str(self.user_id),
        }
        
        response = self.client.put(
            f'/api/events/templates/{template.id}/update/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['name'], 'Updated Name')
        
    def test_delete_template(self):
        """Test deleting template via API."""
        template = EventTemplate.objects.create(
            name='Delete Me',
            description='Test',
            category='other',
            template_data={'title': 'Event', 'description': 'Test'},
            created_by=self.user_id,
        )
        
        response = self.client.delete(
            f'/api/events/templates/{template.id}/delete/?user_id={self.user_id}'
        )
        
        self.assertEqual(response.status_code, 204)
        self.assertFalse(EventTemplate.objects.filter(id=template.id).exists())
        
    def test_clone_template(self):
        """Test cloning template via API."""
        template = EventTemplate.objects.create(
            name='Original',
            description='Original',
            category='social',
            template_data={'title': 'Social Event', 'description': 'Test'},
            created_by=uuid.uuid4(),
            visibility='public',
        )
        
        data = {
            'user_id': str(self.user_id),
            'name': 'My Clone',
        }
        
        response = self.client.post(
            f'/api/events/templates/{template.id}/clone/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        result = response.json()
        self.assertEqual(result['name'], 'My Clone')
