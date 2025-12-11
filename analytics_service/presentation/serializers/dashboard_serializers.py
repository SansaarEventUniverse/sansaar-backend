from rest_framework import serializers
from domain.models import Dashboard, DashboardWidget


class DashboardWidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardWidget
        fields = ['id', 'widget_type', 'title', 'config', 'position', 'is_visible', 'created_at']
        read_only_fields = ['id', 'created_at']


class DashboardSerializer(serializers.ModelSerializer):
    widgets = DashboardWidgetSerializer(many=True, read_only=True)

    class Meta:
        model = Dashboard
        fields = ['id', 'organizer_id', 'name', 'layout', 'is_active', 'widgets', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
