from rest_framework import serializers
from domain.models import CustomReport, ReportTemplate


class CustomReportSerializer(serializers.ModelSerializer):
    metrics_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomReport
        fields = ['id', 'name', 'report_type', 'config', 'metrics_count', 'created_at', 'updated_at']

    def get_metrics_count(self, obj):
        return obj.get_metrics_count()


class ReportTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTemplate
        fields = ['id', 'name', 'template_type', 'template_config', 'is_active', 'created_at']


class BuildReportSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    report_type = serializers.CharField(max_length=50)
    config = serializers.JSONField(required=False, default=dict)


class GenerateReportSerializer(serializers.Serializer):
    report_id = serializers.IntegerField()
