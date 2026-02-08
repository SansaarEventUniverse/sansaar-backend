from rest_framework import serializers
from domain.models import ROIAnalytics, ROIMetric

class ROIAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ROIAnalytics
        fields = '__all__'

class ROIMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = ROIMetric
        fields = '__all__'
