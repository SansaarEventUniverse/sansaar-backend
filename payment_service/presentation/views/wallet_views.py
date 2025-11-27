from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from application.wallet_service import (
    MobileWalletService,
    WalletPaymentService,
    WalletTopUpService
)
from infrastructure.services.wallet_client import WalletPaymentPipeline
from presentation.serializers.wallet_serializers import (
    MobileWalletSerializer,
    WalletPaymentSerializer,
    AddToWalletSerializer,
    WalletStatusSerializer
)


@api_view(['POST'])
def wallet_payment(request):
    """Process wallet payment."""
    serializer = WalletPaymentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        payment_service = WalletPaymentService()
        transaction = payment_service.process_payment(serializer.validated_data)
        
        # Process through wallet pipeline
        wallet_service = MobileWalletService()
        wallet = wallet_service.get_wallet(serializer.validated_data['wallet_id'])
        
        pipeline = WalletPaymentPipeline()
        result = pipeline.process(wallet.wallet_type, {
            'amount': serializer.validated_data['amount'],
            'currency': serializer.validated_data.get('currency', 'USD')
        })
        
        if result['success']:
            transaction.complete(result['transaction_id'])
        
        return Response({
            'transaction_id': str(transaction.id),
            'status': transaction.status,
            'amount': str(transaction.amount)
        }, status=status.HTTP_201_CREATED)
    
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_to_wallet(request, ticket_id):
    """Add ticket to mobile wallet."""
    serializer = AddToWalletSerializer(data={
        'wallet_id': request.data.get('wallet_id'),
        'ticket_id': ticket_id
    })
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        topup_service = WalletTopUpService()
        result = topup_service.add_to_wallet(
            serializer.validated_data['wallet_id'],
            serializer.validated_data['ticket_id']
        )
        
        # Generate wallet pass
        wallet_service = MobileWalletService()
        wallet = wallet_service.get_wallet(serializer.validated_data['wallet_id'])
        
        pipeline = WalletPaymentPipeline()
        pass_data = pipeline.generate_pass(wallet.wallet_type, {
            'ticket_id': str(ticket_id)
        })
        
        return Response({
            'status': result['status'],
            'pass_url': pass_data['pass_url']
        }, status=status.HTTP_200_OK)
    
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def wallet_status(request, wallet_id):
    """Get wallet status."""
    try:
        wallet_service = MobileWalletService()
        wallet = wallet_service.get_wallet(wallet_id)
        
        serializer = WalletStatusSerializer({
            'id': wallet.id,
            'status': wallet.status,
            'wallet_type': wallet.wallet_type,
            'last_used': wallet.last_used
        })
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
