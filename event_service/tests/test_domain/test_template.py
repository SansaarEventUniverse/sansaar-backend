import uuid
from django.test import TestCase
from django.core.exceptions import ValidationError

from domain.template import EventTemplate


class EventTemplateTest(TestCase):
    """Tests for EventTemplate model."""
    
    def test_create_template(self):
        """Test creating event template."""
        template = EventTemplate.objects.create(
            name='Conference Template',
            description='Standard conference template',
            category='conference',
            template_data={
                'title': 'Annual Conference',
                'description': 'Conference description',
                'duration_hours': 8,
            },
            created_by=uuid.uuid4(),
        )
        
        self.assertEqual(template.version, 1)
        self.assertEqual(template.visibility, 'private')
        self.assertEqual(template.usage_count, 0)
        
    def test_validate_template_data(self):
        """Test template data validation."""
        template = EventTemplate(
            name='Invalid Template',
            description='Missing required fields',
            category='workshop',
            template_data={'duration': 2},
            created_by=uuid.uuid4(),
        )
        
        with self.assertRaises(ValidationError):
            template.validate_template_data()
            
    def test_can_access_public(self):
        """Test access control for public template."""
        template = EventTemplate.objects.create(
            name='Public Template',
            description='Public template',
            category='meetup',
            template_data={'title': 'Meetup', 'description': 'Test'},
            created_by=uuid.uuid4(),
            visibility='public',
        )
        
        self.assertTrue(template.can_access(uuid.uuid4()))
        
    def test_can_access_organization(self):
        """Test access control for organization template."""
        org_id = uuid.uuid4()
        template = EventTemplate.objects.create(
            name='Org Template',
            description='Organization template',
            category='conference',
            template_data={'title': 'Event', 'description': 'Test'},
            created_by=uuid.uuid4(),
            organization_id=org_id,
            visibility='organization',
        )
        
        self.assertTrue(template.can_access(uuid.uuid4(), org_id))
        self.assertFalse(template.can_access(uuid.uuid4(), uuid.uuid4()))
        
    def test_can_access_private(self):
        """Test access control for private template."""
        user_id = uuid.uuid4()
        template = EventTemplate.objects.create(
            name='Private Template',
            description='Private template',
            category='workshop',
            template_data={'title': 'Workshop', 'description': 'Test'},
            created_by=user_id,
            visibility='private',
        )
        
        self.assertTrue(template.can_access(user_id))
        self.assertFalse(template.can_access(uuid.uuid4()))
        
    def test_increment_usage(self):
        """Test incrementing usage count."""
        template = EventTemplate.objects.create(
            name='Test Template',
            description='Test',
            category='webinar',
            template_data={'title': 'Webinar', 'description': 'Test'},
            created_by=uuid.uuid4(),
        )
        
        self.assertEqual(template.usage_count, 0)
        template.increment_usage()
        self.assertEqual(template.usage_count, 1)
        
    def test_create_new_version(self):
        """Test creating new version of template."""
        template = EventTemplate.objects.create(
            name='Versioned Template',
            description='Original version',
            category='conference',
            template_data={'title': 'Event v1', 'description': 'Test'},
            created_by=uuid.uuid4(),
        )
        
        new_data = {'title': 'Event v2', 'description': 'Updated'}
        new_template = template.create_new_version(new_data, uuid.uuid4())
        
        self.assertEqual(new_template.version, 2)
        self.assertEqual(new_template.parent_template_id, template.id)
        self.assertEqual(new_template.template_data['title'], 'Event v2')
        
    def test_clone_template(self):
        """Test cloning template."""
        template = EventTemplate.objects.create(
            name='Original Template',
            description='Original',
            category='meetup',
            template_data={'title': 'Meetup', 'description': 'Test'},
            created_by=uuid.uuid4(),
            visibility='public',
        )
        
        cloned = template.clone_template(uuid.uuid4(), 'My Custom Template')
        
        self.assertEqual(cloned.name, 'My Custom Template')
        self.assertEqual(cloned.visibility, 'private')
        self.assertEqual(cloned.parent_template_id, template.id)
        self.assertEqual(cloned.template_data, template.template_data)
