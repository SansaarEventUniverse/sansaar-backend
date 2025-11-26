from rest_framework import serializers


class MobileWalletSerializer(serializers.Serializer):
    """Serializer for mobile wallet."""
    id = serializers.UUIDField(read_only=True)
    user_id = serializers.UUIDField()
    wallet_type = serializers.ChoiceField(choices=['apple_pay', 'google_pay'])
    wallet_token = serializers.CharField(max_length=255)
    device_id = serializers.CharField(max_length=255)
    status = serializers.CharField(read_only=True)
    last_used = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class WalletPaymentSerializer(serializers.Serializer):
    """Serializer for wallet payment."""
    wallet_id = serializers.UUIDField()
    order_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3, default='USD')


class AddToWalletSerializer(serializers.Serializer):
    """Serializer for adding ticket to wallet."""
    wallet_id = serializers.UUIDField()
    ticket_id = serializers.UUIDField()


class WalletStatusSerializer(serializers.Serializer):
    """Serializer for wallet status."""
    id = serializers.UUIDField()
    status = serializers.CharField()
    wallet_type = serializers.CharField()
    last_used = serializers.DateTimeField()
