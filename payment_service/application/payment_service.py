import uuid
from decimal import Decimal
from typing import Dict, Any
from django.core.exceptions import ValidationError
from domain.payment import Payment, PaymentMethod


class ProcessPaymentService:
    """Service for processing payments."""
    
    def execute(self, data: Dict[str, Any]) -> Payment:
        """Process a payment."""
        try:
            payment_method = PaymentMethod.objects.get(id=data['payment_method_id'])
        except PaymentMethod.DoesNotExist:
            raise ValidationError("Payment method not found")
        
        if not payment_method.is_active:
            raise ValidationError("Payment method is not active")
        
        payment = Payment.objects.create(
            order_id=data['order_id'],
            payment_method=payment_method,
            amount=data['amount'],
            currency=data.get('currency', payment_method.currency)
        )
        payment.clean()
        return payment


class RefundPaymentService:
    """Service for refunding payments."""
    
    def execute(self, payment_id: uuid.UUID, amount: Decimal, reason: str = '') -> Payment:
        """Process a refund."""
        try:
            payment = Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:
            raise ValidationError("Payment not found")
        
        payment.refund(amount, reason)
        return payment


class PaymentValidationService:
    """Service for validating payments."""
    
    def validate_payment_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate payment data."""
        errors = {}
        
        if 'order_id' not in data:
            errors['order_id'] = 'Order ID is required'
        
        if 'payment_method_id' not in data:
            errors['payment_method_id'] = 'Payment method ID is required'
        
        if 'amount' not in data:
            errors['amount'] = 'Amount is required'
        elif data['amount'] <= 0:
            errors['amount'] = 'Amount must be positive'
        
        if errors:
            raise ValidationError(errors)
        
        return data
