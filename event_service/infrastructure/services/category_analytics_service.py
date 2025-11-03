from typing import Dict, Any, List
from django.db.models import Count

from domain.category import Category, Tag


class CategoryAnalyticsService:
    """Service for category analytics."""
    
    def get_category_stats(self) -> Dict[str, Any]:
        """Get category statistics."""
        total_categories = Category.objects.filter(is_active=True).count()
        root_categories = Category.objects.filter(parent=None, is_active=True).count()
        
        top_categories = list(
            Category.objects.filter(is_active=True)
            .order_by('-event_count')[:10]
            .values('name', 'event_count')
        )
        
        return {
            'total_categories': total_categories,
            'root_categories': root_categories,
            'top_categories': top_categories,
        }


class TagAnalyticsService:
    """Service for tag analytics."""
    
    def get_tag_stats(self) -> Dict[str, Any]:
        """Get tag statistics."""
        total_tags = Tag.objects.count()
        featured_tags = Tag.objects.filter(is_featured=True).count()
        
        top_tags = list(
            Tag.objects.order_by('-usage_count')[:20]
            .values('name', 'usage_count')
        )
        
        return {
            'total_tags': total_tags,
            'featured_tags': featured_tags,
            'top_tags': top_tags,
        }
    
    def get_trending_tags(self, limit: int = 10) -> List[Tag]:
        """Get trending tags."""
        return list(
            Tag.objects.filter(usage_count__gt=0)
            .order_by('-usage_count')[:limit]
        )
