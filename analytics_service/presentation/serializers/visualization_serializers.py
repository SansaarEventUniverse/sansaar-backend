from rest_framework import serializers
from domain.models import Visualization, Chart


class VisualizationSerializer(serializers.ModelSerializer):
    chart_count = serializers.SerializerMethodField()

    class Meta:
        model = Visualization
        fields = ['id', 'name', 'visualization_type', 'config', 'chart_count', 'created_at', 'updated_at']

    def get_chart_count(self, obj):
        return obj.get_chart_count()


class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chart
        fields = ['id', 'visualization', 'chart_type', 'data', 'config', 'created_at']


class ChartCreateSerializer(serializers.Serializer):
    visualization_id = serializers.IntegerField()
    chart_type = serializers.CharField(max_length=50)
    data = serializers.JSONField()
    config = serializers.JSONField(required=False, default=dict)
