from rest_framework import serializers
from domain.models import PersonalizationRule, UserPreference

class PersonalizationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalizationRule
        fields = '__all__'

class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = '__all__'

class PersonalizeContentSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    content = serializers.JSONField()
