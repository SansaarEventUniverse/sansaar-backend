from rest_framework import serializers
from domain.tax import TaxRule, TaxCalculation


class TaxRuleSerializer(serializers.ModelSerializer):
    """Serializer for tax rule responses."""
    
    class Meta:
        model = TaxRule
        fields = ['id', 'name', 'country', 'state', 'tax_type', 'tax_rate', 'is_active', 'created_at']


class TaxCalculationSerializer(serializers.ModelSerializer):
    """Serializer for tax calculation responses."""
    
    class Meta:
        model = TaxCalculation
        fields = ['id', 'order_id', 'tax_rule_id', 'subtotal', 'tax_amount', 'total', 'currency', 'created_at']


class CalculateTaxRequestSerializer(serializers.Serializer):
    """Serializer for tax calculation requests."""
    country = serializers.CharField(max_length=2, default='US')
    state = serializers.CharField(max_length=50, required=False, allow_blank=True)
