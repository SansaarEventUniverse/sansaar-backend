from rest_framework import serializers
from domain.models import FinancialReport, RevenueAnalytics


class FinancialReportSerializer(serializers.ModelSerializer):
    profit_margin = serializers.SerializerMethodField()

    class Meta:
        model = FinancialReport
        fields = ['event_id', 'total_revenue', 'total_expenses', 'net_profit', 'profit_margin', 'created_at', 'updated_at']

    def get_profit_margin(self, obj):
        return obj.calculate_profit_margin()


class RevenueAnalyticsSerializer(serializers.ModelSerializer):
    revenue_breakdown = serializers.SerializerMethodField()

    class Meta:
        model = RevenueAnalytics
        fields = ['event_id', 'ticket_revenue', 'sponsorship_revenue', 'total_revenue', 'revenue_breakdown', 'created_at', 'updated_at']

    def get_revenue_breakdown(self, obj):
        return obj.calculate_revenue_breakdown()
