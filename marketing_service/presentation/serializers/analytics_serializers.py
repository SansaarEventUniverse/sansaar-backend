from rest_framework import serializers
from domain.models import CampaignAnalytics, PerformanceMetric

class CampaignAnalyticsSerializer(serializers.ModelSerializer):
    open_rate = serializers.SerializerMethodField()
    click_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = CampaignAnalytics
        fields = '__all__'
    
    def get_open_rate(self, obj):
        return obj.calculate_open_rate()
    
    def get_click_rate(self, obj):
        return obj.calculate_click_rate()

class PerformanceMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceMetric
        fields = '__all__'
