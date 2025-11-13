from rest_framework import serializers

from domain.template import EventTemplate


class EventTemplateSerializer(serializers.ModelSerializer):
    """Serializer for EventTemplate."""
    
    class Meta:
        model = EventTemplate
        fields = [
            'id', 'name', 'description', 'category', 'template_data',
            'visibility', 'is_featured', 'version', 'usage_count',
            'created_at', 'updated_at'
        ]


class CreateTemplateSerializer(serializers.Serializer):
    """Serializer for creating template."""
    
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=2000)
    category = serializers.ChoiceField(choices=EventTemplate.CATEGORY_CHOICES)
    template_data = serializers.JSONField()
    visibility = serializers.ChoiceField(
        choices=EventTemplate.VISIBILITY_CHOICES, 
        default='private'
    )
    organization_id = serializers.UUIDField(required=False, allow_null=True)
    created_by = serializers.UUIDField()


class ApplyTemplateSerializer(serializers.Serializer):
    """Serializer for applying template."""
    
    template_id = serializers.UUIDField()
    event_data = serializers.JSONField()
    user_id = serializers.UUIDField()
