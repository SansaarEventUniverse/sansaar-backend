from rest_framework import serializers
from domain.subscription import Subscription, RecurringPayment


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for Subscription model."""
    
    class Meta:
        model = Subscription
        fields = [
            'id', 'user_id', 'plan_name', 'amount', 'billing_cycle',
            'status', 'start_date', 'next_billing_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'start_date']


class CreateSubscriptionSerializer(serializers.Serializer):
    """Serializer for creating a subscription."""
    
    user_id = serializers.UUIDField()
    plan_name = serializers.CharField(max_length=255)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = serializers.ChoiceField(
        choices=['monthly', 'quarterly', 'yearly']
    )


class ManageSubscriptionSerializer(serializers.Serializer):
    """Serializer for managing subscription actions."""
    
    action = serializers.ChoiceField(choices=['pause', 'cancel'])


class RecurringPaymentSerializer(serializers.ModelSerializer):
    """Serializer for RecurringPayment model."""
    
    class Meta:
        model = RecurringPayment
        fields = [
            'id', 'subscription_id', 'amount', 'status',
            'billing_date', 'payment_method', 'transaction_id',
            'created_at', 'processed_at'
        ]
        read_only_fields = ['id', 'created_at', 'processed_at']
