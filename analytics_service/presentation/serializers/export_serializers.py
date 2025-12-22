from rest_framework import serializers
from domain.models import DataExport, ExportTemplate


class DataExportSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = DataExport
        fields = ['id', 'export_name', 'export_format', 'status', 'file_path', 'is_completed', 'created_at']

    def get_is_completed(self, obj):
        return obj.is_completed()


class ExportTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportTemplate
        fields = ['id', 'template_name', 'export_format', 'config', 'is_active', 'created_at']


class ExportDataSerializer(serializers.Serializer):
    export_name = serializers.CharField(max_length=200)
    export_format = serializers.CharField(max_length=50)
    data = serializers.JSONField()


class ScheduleExportSerializer(serializers.Serializer):
    export_name = serializers.CharField(max_length=200)
    export_format = serializers.CharField(max_length=50)
    schedule = serializers.CharField(max_length=50)
