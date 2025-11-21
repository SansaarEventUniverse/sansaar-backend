from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
import uuid

from application.refund_service import ProcessRefundService
from domain.refund import Refund
from presentation.serializers.refund_serializers import (
    RequestRefundSerializer,
    ProcessRefundSerializer,
    RefundSerializer
)


class RequestRefundView(APIView):
    """Request a refund for a ticket."""
    
    def post(self, request):
        serializer = RequestRefundSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service = ProcessRefundService()
            refund = service.execute(serializer.validated_data)
            response_serializer = RefundSerializer(refund)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error': e.messages[0] if hasattr(e, 'messages') else str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProcessRefundView(APIView):
    """Process a refund (approve/reject)."""
    
    def post(self, request, refund_id):
        serializer = ProcessRefundSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refund = Refund.objects.get(id=uuid.UUID(refund_id))
        except Refund.DoesNotExist:
            return Response({'error': 'Refund not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            action = serializer.validated_data['action']
            
            if action == 'approve':
                refund.process()
                refund.complete()
                message = 'Refund approved and processed'
            else:
                reason = serializer.validated_data.get('rejection_reason', 'No reason provided')
                refund.reject(reason)
                message = 'Refund rejected'
            
            response_serializer = RefundSerializer(refund)
            return Response({
                'message': message,
                'refund': response_serializer.data
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': e.messages[0] if hasattr(e, 'messages') else str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetRefundStatusView(APIView):
    """Get refund status."""
    
    def get(self, request, refund_id):
        try:
            refund = Refund.objects.get(id=uuid.UUID(refund_id))
            serializer = RefundSerializer(refund)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Refund.DoesNotExist:
            return Response({'error': 'Refund not found'}, status=status.HTTP_404_NOT_FOUND)
