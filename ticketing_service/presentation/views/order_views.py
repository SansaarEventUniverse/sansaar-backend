from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
import uuid

from application.order_service import (
    CreateOrderService,
    ProcessTicketPurchaseService,
    OrderManagementService
)
from presentation.serializers.order_serializers import (
    CreateOrderSerializer,
    ProcessPurchaseSerializer,
    OrderSerializer
)


class CreateOrderView(APIView):
    """Create a new order."""
    
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service = CreateOrderService()
            order = service.execute(serializer.validated_data)
            response_serializer = OrderSerializer(order)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProcessPurchaseView(APIView):
    """Process a ticket purchase."""
    
    def post(self, request, order_id):
        serializer = ProcessPurchaseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service = ProcessTicketPurchaseService()
            tickets = service.execute(
                uuid.UUID(order_id),
                serializer.validated_data['payment_id']
            )
            return Response({
                'message': 'Purchase processed successfully',
                'tickets_generated': len(tickets)
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetOrderView(APIView):
    """Get order details."""
    
    def get(self, request, order_id):
        try:
            service = OrderManagementService()
            order = service.get_order(uuid.UUID(order_id))
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
