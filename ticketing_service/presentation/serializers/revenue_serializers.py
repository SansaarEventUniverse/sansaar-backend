from rest_framework import serializers
from domain.revenue import Revenue, RevenueReport


class RevenueSerializer(serializers.ModelSerializer):
    """Serializer for revenue responses."""
    
    class Meta:
        model = Revenue
        fields = ['id', 'event_id', 'order_id', 'gross_amount', 'platform_fee',
                  'payment_fee', 'net_amount', 'currency', 'created_at']


class RevenueReportSerializer(serializers.ModelSerializer):
    """Serializer for revenue report responses."""
    
    class Meta:
        model = RevenueReport
        fields = ['id', 'event_id', 'period', 'start_date', 'end_date',
                  'total_gross', 'total_fees', 'total_net', 'total_orders',
                  'total_refunds', 'created_at']


class PayoutSerializer(serializers.Serializer):
    """Serializer for payout responses."""
    event_id = serializers.UUIDField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_refunds = serializers.DecimalField(max_digits=10, decimal_places=2)
    payout_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField()
