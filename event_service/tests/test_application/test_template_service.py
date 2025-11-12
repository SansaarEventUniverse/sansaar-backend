import uuid
from datetime import datetime
from django.test import TestCase
from django.core.exceptions import ValidationError
import pytz

from domain.template import EventTemplate
from domain.event import Event
from application.template_service import (
    CreateTemplateService,
    ApplyTemplateService,
    TemplateManagementService,
)


class CreateTemplateServiceTest(TestCase):
    """Tests for CreateTemplateService."""
    
    def test_create_from_event(self):
        """Test creating template from event."""
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            start_datetime=datetime(2026, 2, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 2, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=uuid.uuid4(),
        )
        
        service = CreateTemplateService()
        template = service.create_from_event(
            event.id, 'Event Template', 'Template from event', uuid.uuid4()
        )
        
        self.assertEqual(template.name, 'Event Template')
        self.assertIn('title', template.template_data)
        
    def test_create_custom(self):
        """Test creating custom template."""
        service = CreateTemplateService()
        template = service.create_custom({
            'name': 'Custom Template',
            'description': 'Custom',
            'category': 'workshop',
            'template_data': {'title': 'Workshop', 'description': 'Test'},
            'created_by': uuid.uuid4(),
        })
        
        self.assertEqual(template.name, 'Custom Template')


class ApplyTemplateServiceTest(TestCase):
    """Tests for ApplyTemplateService."""
    
    def test_apply_to_event(self):
        """Test applying template to event."""
        user_id = uuid.uuid4()
        template = EventTemplate.objects.create(
            name='Test Template',
            description='Test',
            category='conference',
            template_data={'title': 'Conference', 'description': 'Test', 'duration': 8},
            created_by=user_id,
            visibility='public',
        )
        
        service = ApplyTemplateService()
        merged = service.apply_to_event(
            template.id,
            {'title': 'My Conference', 'location': 'NYC'},
            user_id
        )
        
        self.assertEqual(merged['title'], 'My Conference')
        self.assertEqual(merged['duration'], 8)
        self.assertEqual(merged['location'], 'NYC')
        
        template.refresh_from_db()
        self.assertEqual(template.usage_count, 1)
        
    def test_preview_template(self):
        """Test previewing template."""
        user_id = uuid.uuid4()
        template = EventTemplate.objects.create(
            name='Preview Template',
            description='Test',
            category='meetup',
            template_data={'title': 'Meetup', 'description': 'Test'},
            created_by=user_id,
            visibility='public',
        )
        
        service = ApplyTemplateService()
        preview = service.preview_template(template.id, user_id)
        
        self.assertEqual(preview['title'], 'Meetup')


class TemplateManagementServiceTest(TestCase):
    """Tests for TemplateManagementService."""
    
    def test_get_templates(self):
        """Test getting accessible templates."""
        user_id = uuid.uuid4()
        EventTemplate.objects.create(
            name='Public Template',
            description='Public',
            category='conference',
            template_data={'title': 'Event', 'description': 'Test'},
            created_by=uuid.uuid4(),
            visibility='public',
        )
        EventTemplate.objects.create(
            name='Private Template',
            description='Private',
            category='workshop',
            template_data={'title': 'Workshop', 'description': 'Test'},
            created_by=user_id,
            visibility='private',
        )
        
        service = TemplateManagementService()
        templates = service.get_templates(user_id)
        
        self.assertEqual(len(templates), 2)
        
    def test_get_featured_templates(self):
        """Test getting featured templates."""
        EventTemplate.objects.create(
            name='Featured Template',
            description='Featured',
            category='webinar',
            template_data={'title': 'Webinar', 'description': 'Test'},
            created_by=uuid.uuid4(),
            visibility='public',
            is_featured=True,
        )
        
        service = TemplateManagementService()
        featured = service.get_featured_templates()
        
        self.assertEqual(len(featured), 1)
        
    def test_update_template(self):
        """Test updating template."""
        user_id = uuid.uuid4()
        template = EventTemplate.objects.create(
            name='Original Name',
            description='Original',
            category='meetup',
            template_data={'title': 'Meetup', 'description': 'Test'},
            created_by=user_id,
        )
        
        service = TemplateManagementService()
        updated = service.update_template(
            template.id, {'name': 'Updated Name'}, user_id
        )
        
        self.assertEqual(updated.name, 'Updated Name')
        
    def test_clone_template(self):
        """Test cloning template."""
        template = EventTemplate.objects.create(
            name='Original',
            description='Original',
            category='conference',
            template_data={'title': 'Conference', 'description': 'Test'},
            created_by=uuid.uuid4(),
            visibility='public',
        )
        
        service = TemplateManagementService()
        cloned = service.clone_template(template.id, uuid.uuid4(), 'My Clone')
        
        self.assertEqual(cloned.name, 'My Clone')
        self.assertEqual(cloned.parent_template_id, template.id)
