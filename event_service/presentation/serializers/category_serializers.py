from rest_framework import serializers

from domain.category import Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category."""
    
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'parent', 'event_count', 'children']
    
    def get_children(self, obj):
        if hasattr(obj, '_prefetched_objects_cache') and 'children' in obj._prefetched_objects_cache:
            return CategorySerializer(obj.children.filter(is_active=True), many=True).data
        return []


class CreateCategorySerializer(serializers.Serializer):
    """Serializer for creating categories."""
    
    name = serializers.CharField(max_length=100)
    slug = serializers.SlugField(max_length=100, required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    parent_id = serializers.UUIDField(required=False, allow_null=True)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag."""
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'usage_count', 'is_featured']


class CreateTagSerializer(serializers.Serializer):
    """Serializer for creating tags."""
    
    name = serializers.CharField(max_length=50)
