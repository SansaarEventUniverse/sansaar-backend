from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid

from application.fraud_service import RiskAssessmentService
from infrastructure.repositories.fraud_repository import FraudRepository
from domain.order import Order
from presentation.serializers.fraud_serializers import FraudAlertSerializer


class FraudAlertView(APIView):
    """Get fraud alerts."""
    
    def get(self, request):
        repository = FraudRepository()
        alerts = repository.get_open_alerts()
        
        serializer = FraudAlertSerializer(alerts, many=True)
        
        return Response({
            'alerts': serializer.data,
            'total_count': len(alerts)
        }, status=status.HTTP_200_OK)


class SecurityReportView(APIView):
    """Get security report."""
    
    def get(self, request):
        repository = FraudRepository()
        analytics = repository.get_fraud_analytics()
        
        return Response(analytics, status=status.HTTP_200_OK)


class RiskAssessmentView(APIView):
    """Assess order risk."""
    
    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=uuid.UUID(order_id))
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        
        service = RiskAssessmentService()
        assessment = service.assess_order(order)
        
        return Response(assessment, status=status.HTTP_200_OK)
