import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from application.payment_service import (
    ProcessPaymentService,
    RefundPaymentService,
    PaymentValidationService
)
from domain.payment import Payment
from presentation.serializers.payment_serializers import (
    PaymentSerializer,
    ProcessPaymentSerializer,
    RefundPaymentSerializer
)


@api_view(['POST'])
def process_payment(request):
    """Process a payment."""
    serializer = ProcessPaymentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        validation_service = PaymentValidationService()
        validation_service.validate_payment_data(serializer.validated_data)
        
        service = ProcessPaymentService()
        payment = service.execute(serializer.validated_data)
        
        return Response(
            PaymentSerializer(payment).data,
            status=status.HTTP_201_CREATED
        )
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def refund_payment(request, payment_id):
    """Refund a payment."""
    try:
        payment_uuid = uuid.UUID(payment_id)
    except ValueError:
        return Response({'error': 'Invalid payment ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = RefundPaymentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = RefundPaymentService()
        payment = service.execute(
            payment_uuid,
            serializer.validated_data['amount'],
            serializer.validated_data.get('reason', '')
        )
        return Response(PaymentSerializer(payment).data)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_payment(request, payment_id):
    """Get payment details."""
    try:
        payment_uuid = uuid.UUID(payment_id)
    except ValueError:
        return Response({'error': 'Invalid payment ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        payment = Payment.objects.get(id=payment_uuid)
        return Response(PaymentSerializer(payment).data)
    except Payment.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
