from rest_framework import serializers
from domain.models import SocialMediaPost, SocialPlatform

class SocialMediaPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaPost
        fields = '__all__'

class SocialPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialPlatform
        fields = '__all__'

class SchedulePostSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    scheduled_at = serializers.DateTimeField()
