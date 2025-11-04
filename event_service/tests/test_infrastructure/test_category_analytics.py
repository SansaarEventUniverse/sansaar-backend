from django.test import TestCase

from domain.category import Category, Tag
from infrastructure.services.category_analytics_service import (
    CategoryAnalyticsService,
    TagAnalyticsService,
)


class CategoryAnalyticsServiceTest(TestCase):
    """Tests for CategoryAnalyticsService."""
    
    def test_get_category_stats(self):
        """Test getting category statistics."""
        Category.objects.create(name='Technology', slug='technology', event_count=10)
        Category.objects.create(name='Music', slug='music', event_count=5)
        
        service = CategoryAnalyticsService()
        stats = service.get_category_stats()
        
        self.assertEqual(stats['total_categories'], 2)
        self.assertEqual(stats['root_categories'], 2)
        self.assertEqual(len(stats['top_categories']), 2)


class TagAnalyticsServiceTest(TestCase):
    """Tests for TagAnalyticsService."""
    
    def test_get_tag_stats(self):
        """Test getting tag statistics."""
        Tag.objects.create(name='python', slug='python', usage_count=100)
        Tag.objects.create(name='django', slug='django', usage_count=50, is_featured=True)
        
        service = TagAnalyticsService()
        stats = service.get_tag_stats()
        
        self.assertEqual(stats['total_tags'], 2)
        self.assertEqual(stats['featured_tags'], 1)
        self.assertEqual(len(stats['top_tags']), 2)
        
    def test_get_trending_tags(self):
        """Test getting trending tags."""
        Tag.objects.create(name='python', slug='python', usage_count=100)
        Tag.objects.create(name='django', slug='django', usage_count=50)
        
        service = TagAnalyticsService()
        trending = service.get_trending_tags(limit=10)
        
        self.assertEqual(len(trending), 2)
        self.assertEqual(trending[0].name, 'python')
