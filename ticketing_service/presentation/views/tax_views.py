from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
import uuid

from application.tax_service import (
    TaxCalculationService,
    TaxComplianceService,
    TaxReportingService
)
from domain.order import Order
from presentation.serializers.tax_serializers import (
    TaxCalculationSerializer,
    CalculateTaxRequestSerializer
)


class CalculateTaxView(APIView):
    """Calculate tax for an order."""
    
    def post(self, request, order_id):
        serializer = CalculateTaxRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            order = Order.objects.get(id=uuid.UUID(order_id))
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        
        service = TaxCalculationService()
        calc = service.calculate_for_order(
            order,
            serializer.validated_data['country'],
            serializer.validated_data.get('state', '')
        )
        
        response_serializer = TaxCalculationSerializer(calc)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class GetTaxReportView(APIView):
    """Get tax report for an event."""
    
    def get(self, request, event_id):
        service = TaxReportingService()
        report = service.generate_report(uuid.UUID(event_id))
        
        return Response(report, status=status.HTTP_200_OK)


class TaxComplianceView(APIView):
    """Get tax compliance status for an event."""
    
    def get(self, request, event_id):
        service = TaxComplianceService()
        compliance = service.check_compliance(uuid.UUID(event_id))
        
        return Response(compliance, status=status.HTTP_200_OK)
