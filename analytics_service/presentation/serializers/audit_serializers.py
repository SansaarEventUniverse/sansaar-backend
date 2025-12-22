from rest_framework import serializers
from domain.models import AuditTrail, ComplianceReport


class AuditTrailSerializer(serializers.ModelSerializer):
    is_successful = serializers.SerializerMethodField()

    class Meta:
        model = AuditTrail
        fields = ['id', 'user_id', 'action', 'resource', 'status', 'metadata', 'is_successful', 'created_at']

    def get_is_successful(self, obj):
        return obj.is_successful()


class ComplianceReportSerializer(serializers.ModelSerializer):
    is_compliant = serializers.SerializerMethodField()

    class Meta:
        model = ComplianceReport
        fields = ['id', 'report_type', 'status', 'findings', 'is_compliant', 'created_at']

    def get_is_compliant(self, obj):
        return obj.is_compliant()


class AuditSearchSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=100, required=False)
    user_id = serializers.CharField(max_length=100, required=False)
