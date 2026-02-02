from rest_framework import serializers
from domain.models import MarketingIntelligence, IntelligenceInsight

class MarketingIntelligenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketingIntelligence
        fields = '__all__'

class IntelligenceInsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntelligenceInsight
        fields = '__all__'
