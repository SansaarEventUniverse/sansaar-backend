from rest_framework import serializers

from domain.registration_form import RegistrationForm, CustomField


class CustomFieldSerializer(serializers.ModelSerializer):
    """Serializer for CustomField."""
    
    class Meta:
        model = CustomField
        fields = ['id', 'label', 'field_type', 'is_required', 'order', 'options']


class RegistrationFormSerializer(serializers.ModelSerializer):
    """Serializer for RegistrationForm."""
    
    fields = CustomFieldSerializer(many=True, read_only=True)
    
    class Meta:
        model = RegistrationForm
        fields = ['id', 'event_id', 'title', 'description', 'is_active', 'fields']


class CreateFormSerializer(serializers.Serializer):
    """Serializer for creating forms."""
    
    title = serializers.CharField(max_length=255)
    fields = serializers.ListField(child=serializers.DictField())


class SubmitFormSerializer(serializers.Serializer):
    """Serializer for form submission."""
    
    data = serializers.DictField()
