import uuid
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.dateparse import parse_datetime
from application.analytics_service import (
    TicketAnalyticsService,
    SalesReportingService,
    BusinessIntelligenceService
)
from presentation.serializers.analytics_serializers import (
    TicketAnalyticsSerializer,
    SalesMetricsSerializer
)


class GetAnalyticsView(APIView):
    """API view for getting ticket analytics."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.analytics_service = TicketAnalyticsService()
    
    def get(self, request, event_id):
        """Get ticket analytics for an event."""
        try:
            analytics_data = self.analytics_service.get_event_analytics(event_id)
            
            if not analytics_data:
                return Response(
                    {'error': 'Analytics not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            return Response(analytics_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SalesReportView(APIView):
    """API view for getting sales report."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reporting_service = SalesReportingService()
    
    def get(self, request, event_id):
        """Get sales report for a period."""
        try:
            start_str = request.query_params.get('start')
            end_str = request.query_params.get('end')
            
            if not start_str or not end_str:
                return Response(
                    {'error': 'start and end parameters are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            period_start = parse_datetime(start_str)
            period_end = parse_datetime(end_str)
            
            report = self.reporting_service.get_period_report(
                event_id,
                period_start,
                period_end
            )
            
            if not report:
                return Response(
                    {'error': 'Report not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            return Response(report, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BusinessIntelligenceView(APIView):
    """API view for business intelligence."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bi_service = BusinessIntelligenceService()
    
    def get(self, request, event_id):
        """Get comprehensive business intelligence."""
        try:
            metrics = self.bi_service.get_comprehensive_metrics(event_id)
            return Response(metrics, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
