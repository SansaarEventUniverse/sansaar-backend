from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid

from application.revenue_service import RevenueReportService, PayoutManagementService
from infrastructure.repositories.revenue_repository import RevenueRepository
from presentation.serializers.revenue_serializers import (
    RevenueSerializer,
    RevenueReportSerializer,
    PayoutSerializer
)


class GetRevenueView(APIView):
    """Get revenue for an event."""
    
    def get(self, request, event_id):
        repository = RevenueRepository()
        
        # Get revenue list
        revenues = repository.get_event_revenue(uuid.UUID(event_id))
        
        # Get analytics
        analytics = repository.get_revenue_analytics(uuid.UUID(event_id))
        
        serializer = RevenueSerializer(revenues, many=True)
        
        return Response({
            'revenues': serializer.data,
            'analytics': analytics
        }, status=status.HTTP_200_OK)


class GenerateReportView(APIView):
    """Generate revenue report for an event."""
    
    def get(self, request, event_id):
        period = request.query_params.get('period', 'daily')
        
        service = RevenueReportService()
        report = service.generate_report(uuid.UUID(event_id), period)
        
        serializer = RevenueReportSerializer(report)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProcessPayoutView(APIView):
    """Process payout for an event."""
    
    def post(self, request, event_id):
        service = PayoutManagementService()
        payout = service.calculate_payout(uuid.UUID(event_id))
        
        serializer = PayoutSerializer(payout)
        
        return Response({
            'message': 'Payout calculated successfully',
            'payout': serializer.data
        }, status=status.HTTP_200_OK)
