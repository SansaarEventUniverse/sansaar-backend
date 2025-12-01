from rest_framework import serializers
from domain.analytics import TicketAnalytics, SalesMetrics


class TicketAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for TicketAnalytics model."""
    
    sold_percentage = serializers.SerializerMethodField()
    average_price = serializers.SerializerMethodField()
    is_sold_out = serializers.SerializerMethodField()
    
    class Meta:
        model = TicketAnalytics
        fields = [
            'id', 'event_id', 'total_tickets', 'sold_tickets', 'revenue',
            'sold_percentage', 'average_price', 'is_sold_out',
            'created_at', 'updated_at'
        ]
    
    def get_sold_percentage(self, obj):
        return obj.calculate_sold_percentage()
    
    def get_average_price(self, obj):
        return obj.calculate_average_ticket_price()
    
    def get_is_sold_out(self, obj):
        return obj.is_sold_out()


class SalesMetricsSerializer(serializers.ModelSerializer):
    """Serializer for SalesMetrics model."""
    
    average_transaction_value = serializers.SerializerMethodField()
    daily_average = serializers.SerializerMethodField()
    growth_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = SalesMetrics
        fields = [
            'id', 'event_id', 'period_start', 'period_end',
            'total_sales', 'transaction_count', 'previous_period_sales',
            'average_transaction_value', 'daily_average', 'growth_rate',
            'created_at', 'updated_at'
        ]
    
    def get_average_transaction_value(self, obj):
        return obj.calculate_average_transaction_value()
    
    def get_daily_average(self, obj):
        return obj.calculate_daily_average()
    
    def get_growth_rate(self, obj):
        return obj.get_growth_rate()
