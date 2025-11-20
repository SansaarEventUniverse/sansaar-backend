from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
import uuid

from application.promo_code_service import (
    CreatePromoCodeService,
    ValidatePromoCodeService,
    ApplyDiscountService
)
from presentation.serializers.promo_code_serializers import (
    CreatePromoCodeSerializer,
    ValidatePromoCodeSerializer,
    ApplyPromoCodeSerializer,
    PromoCodeSerializer
)


class CreatePromoCodeView(APIView):
    """Create a new promo code."""
    
    def post(self, request, event_id=None):
        serializer = CreatePromoCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            data = serializer.validated_data
            if event_id:
                data['event_id'] = uuid.UUID(event_id)
            
            service = CreatePromoCodeService()
            promo = service.execute(data)
            response_serializer = PromoCodeSerializer(promo)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error': e.messages[0] if hasattr(e, 'messages') else str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ValidatePromoCodeView(APIView):
    """Validate a promo code."""
    
    def post(self, request):
        serializer = ValidatePromoCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service = ValidatePromoCodeService()
            result = service.execute(
                serializer.validated_data['code'],
                serializer.validated_data['order_amount'],
                serializer.validated_data.get('event_id')
            )
            
            return Response({
                'valid': True,
                'discount_amount': str(result['discount_amount']),
                'final_amount': str(result['final_amount']),
                'discount_type': result['discount_type'],
                'discount_value': str(result['discount_value'])
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': e.messages[0] if hasattr(e, 'messages') else str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ApplyPromoCodeView(APIView):
    """Apply promo code to order."""
    
    def post(self, request, order_id):
        serializer = ApplyPromoCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service = ApplyDiscountService()
            order = service.execute(
                uuid.UUID(order_id),
                serializer.validated_data['promo_code']
            )
            
            return Response({
                'message': 'Promo code applied successfully',
                'new_total': str(order.total_amount)
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': e.messages[0] if hasattr(e, 'messages') else str(e)}, status=status.HTTP_400_BAD_REQUEST)
