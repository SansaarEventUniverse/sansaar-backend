from typing import Dict, Any, List
import uuid
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from domain.category import Category, Tag


class CategoryManagementService:
    """Service for managing categories."""
    
    def create_category(self, data: Dict[str, Any]) -> Category:
        """Create a new category."""
        slug = data.get('slug') or slugify(data['name'])
        
        category = Category(
            name=data['name'],
            slug=slug,
            description=data.get('description', ''),
            parent_id=data.get('parent_id'),
        )
        category.clean()
        category.save()
        return category
    
    def get_category_tree(self) -> List[Dict[str, Any]]:
        """Get category hierarchy tree."""
        root_categories = Category.objects.filter(parent=None, is_active=True)
        
        def build_tree(category):
            return {
                'id': str(category.id),
                'name': category.name,
                'slug': category.slug,
                'event_count': category.event_count,
                'children': [build_tree(child) for child in category.children.filter(is_active=True)]
            }
        
        return [build_tree(cat) for cat in root_categories]


class TagManagementService:
    """Service for managing tags."""
    
    def create_tag(self, name: str) -> Tag:
        """Create a new tag."""
        slug = slugify(name)
        
        # Check if tag already exists
        tag, created = Tag.objects.get_or_create(
            slug=slug,
            defaults={'name': name}
        )
        
        if not created:
            tag.increment_usage()
        
        return tag
    
    def get_popular_tags(self, limit: int = 20) -> List[Tag]:
        """Get most popular tags."""
        return list(Tag.objects.all()[:limit])
    
    def suggest_tags(self, query: str, limit: int = 10) -> List[Tag]:
        """Suggest tags based on query."""
        return list(
            Tag.objects.filter(name__icontains=query)[:limit]
        )


class EventCategorizationService:
    """Service for categorizing events."""
    
    def assign_category(self, event_id: uuid.UUID, category_id: uuid.UUID) -> None:
        """Assign category to event."""
        try:
            category = Category.objects.get(id=category_id)
            category.event_count += 1
            category.save()
        except Category.DoesNotExist:
            raise ValidationError('Category not found')
    
    def assign_tags(self, event_id: uuid.UUID, tag_names: List[str]) -> List[Tag]:
        """Assign tags to event."""
        tags = []
        tag_service = TagManagementService()
        
        for name in tag_names:
            tag = tag_service.create_tag(name)
            tags.append(tag)
        
        return tags
