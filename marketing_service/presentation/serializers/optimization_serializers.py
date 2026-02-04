from rest_framework import serializers
from domain.models import CampaignOptimization, OptimizationRule

class CampaignOptimizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignOptimization
        fields = '__all__'

class OptimizationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptimizationRule
        fields = '__all__'
