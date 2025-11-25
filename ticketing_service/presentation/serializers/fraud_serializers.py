from rest_framework import serializers
from domain.fraud import FraudAlert, SecurityRule


class FraudAlertSerializer(serializers.ModelSerializer):
    """Serializer for fraud alert responses."""
    
    class Meta:
        model = FraudAlert
        fields = ['id', 'order_id', 'user_id', 'rule_id', 'severity', 'status',
                  'description', 'risk_score', 'resolved_at', 'created_at']


class SecurityRuleSerializer(serializers.ModelSerializer):
    """Serializer for security rule responses."""
    
    class Meta:
        model = SecurityRule
        fields = ['id', 'name', 'rule_type', 'threshold_value', 'time_window_minutes', 'is_active', 'created_at']
