from django.test import TestCase
from django.core.exceptions import ValidationError

from domain.category import Category, Tag


class CategoryModelTest(TestCase):
    """Tests for Category model."""
    
    def test_create_category(self):
        """Test creating a category."""
        category = Category.objects.create(
            name='Technology',
            slug='technology',
            description='Tech events',
        )
        self.assertIsNotNone(category.id)
        self.assertTrue(category.is_active)
        
    def test_category_hierarchy(self):
        """Test category parent-child relationship."""
        parent = Category.objects.create(name='Technology', slug='technology')
        child = Category.objects.create(
            name='AI & ML',
            slug='ai-ml',
            parent=parent
        )
        
        self.assertEqual(child.parent, parent)
        self.assertIn(child, parent.children.all())
        
    def test_get_ancestors(self):
        """Test getting ancestor categories."""
        grandparent = Category.objects.create(name='Events', slug='events')
        parent = Category.objects.create(name='Technology', slug='technology', parent=grandparent)
        child = Category.objects.create(name='AI', slug='ai', parent=parent)
        
        ancestors = child.get_ancestors()
        self.assertEqual(len(ancestors), 2)
        self.assertIn(parent, ancestors)
        self.assertIn(grandparent, ancestors)
        
    def test_circular_reference_validation(self):
        """Test circular reference prevention."""
        category = Category.objects.create(name='Test', slug='test')
        category.parent = category
        
        with self.assertRaises(ValidationError):
            category.clean()


class TagModelTest(TestCase):
    """Tests for Tag model."""
    
    def test_create_tag(self):
        """Test creating a tag."""
        tag = Tag.objects.create(name='python', slug='python')
        self.assertIsNotNone(tag.id)
        self.assertEqual(tag.usage_count, 0)
        
    def test_increment_usage(self):
        """Test incrementing tag usage."""
        tag = Tag.objects.create(name='django', slug='django')
        tag.increment_usage()
        
        tag.refresh_from_db()
        self.assertEqual(tag.usage_count, 1)
