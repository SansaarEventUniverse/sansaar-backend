import uuid
from django.test import TestCase

from domain.category import Category, Tag
from application.category_service import (
    CategoryManagementService,
    TagManagementService,
    EventCategorizationService,
)


class CategoryManagementServiceTest(TestCase):
    """Tests for CategoryManagementService."""
    
    def test_create_category(self):
        """Test creating a category."""
        service = CategoryManagementService()
        category = service.create_category({
            'name': 'Technology',
            'description': 'Tech events',
        })
        
        self.assertIsNotNone(category.id)
        self.assertEqual(category.slug, 'technology')
        
    def test_get_category_tree(self):
        """Test getting category tree."""
        parent = Category.objects.create(name='Technology', slug='technology')
        Category.objects.create(name='AI', slug='ai', parent=parent)
        
        service = CategoryManagementService()
        tree = service.get_category_tree()
        
        self.assertEqual(len(tree), 1)
        self.assertEqual(tree[0]['name'], 'Technology')
        self.assertEqual(len(tree[0]['children']), 1)


class TagManagementServiceTest(TestCase):
    """Tests for TagManagementService."""
    
    def test_create_tag(self):
        """Test creating a tag."""
        service = TagManagementService()
        tag = service.create_tag('python')
        
        self.assertIsNotNone(tag.id)
        self.assertEqual(tag.slug, 'python')
        
    def test_create_duplicate_tag(self):
        """Test creating duplicate tag increments usage."""
        service = TagManagementService()
        tag1 = service.create_tag('django')
        tag2 = service.create_tag('django')
        
        self.assertEqual(tag1.id, tag2.id)
        tag2.refresh_from_db()
        self.assertEqual(tag2.usage_count, 1)
        
    def test_get_popular_tags(self):
        """Test getting popular tags."""
        Tag.objects.create(name='python', slug='python', usage_count=100)
        Tag.objects.create(name='django', slug='django', usage_count=50)
        
        service = TagManagementService()
        tags = service.get_popular_tags(limit=10)
        
        self.assertEqual(len(tags), 2)
        self.assertEqual(tags[0].name, 'python')


class EventCategorizationServiceTest(TestCase):
    """Tests for EventCategorizationService."""
    
    def test_assign_category(self):
        """Test assigning category to event."""
        category = Category.objects.create(name='Technology', slug='technology')
        
        service = EventCategorizationService()
        service.assign_category(uuid.uuid4(), category.id)
        
        category.refresh_from_db()
        self.assertEqual(category.event_count, 1)
        
    def test_assign_tags(self):
        """Test assigning tags to event."""
        service = EventCategorizationService()
        tags = service.assign_tags(uuid.uuid4(), ['python', 'django'])
        
        self.assertEqual(len(tags), 2)
        self.assertEqual(Tag.objects.count(), 2)
