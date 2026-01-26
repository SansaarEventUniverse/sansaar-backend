from rest_framework import serializers
from domain.models import AudienceSegment, SegmentRule

class AudienceSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudienceSegment
        fields = '__all__'

class SegmentRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SegmentRule
        fields = '__all__'

class AnalyzeAudienceSerializer(serializers.Serializer):
    segment_id = serializers.IntegerField()
