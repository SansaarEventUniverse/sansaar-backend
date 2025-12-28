from rest_framework import serializers
from domain.models import MobileDashboard, MobileWidget


class MobileDashboardSerializer(serializers.ModelSerializer):
    is_responsive = serializers.SerializerMethodField()

    class Meta:
        model = MobileDashboard
        fields = ['id', 'name', 'layout', 'is_optimized', 'is_responsive', 'created_at']

    def get_is_responsive(self, obj):
        return obj.is_responsive()


class MobileWidgetSerializer(serializers.ModelSerializer):
    is_compact = serializers.SerializerMethodField()

    class Meta:
        model = MobileWidget
        fields = ['id', 'dashboard', 'widget_type', 'size', 'position', 'config', 'is_compact']

    def get_is_compact(self, obj):
        return obj.is_compact()
