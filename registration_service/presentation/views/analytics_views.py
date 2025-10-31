import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from application.analytics_service import (
    GenerateAnalyticsService,
    RegistrationReportService,
)
from infrastructure.services.analytics_cache_service import AnalyticsCacheService
from presentation.serializers.analytics_serializers import RegistrationAnalyticsSerializer


@api_view(['GET'])
def get_analytics(request, event_id):
    """Get analytics for event."""
    # Check cache first
    cache_service = AnalyticsCacheService()
    cached = cache_service.get_cached_analytics(uuid.UUID(event_id))
    
    if cached:
        return Response(cached)
    
    # Generate fresh analytics
    service = GenerateAnalyticsService()
    analytics = service.execute(uuid.UUID(event_id))
    
    data = RegistrationAnalyticsSerializer(analytics).data
    
    # Cache the result
    cache_service.cache_analytics(uuid.UUID(event_id), data)
    
    return Response(data)


@api_view(['GET'])
def get_dashboard(request, event_id):
    """Get dashboard data for event."""
    service = RegistrationReportService()
    report = service.execute(uuid.UUID(event_id))
    return Response(report)


@api_view(['GET'])
def export_analytics(request, event_id):
    """Export analytics data."""
    service = RegistrationReportService()
    report = service.execute(uuid.UUID(event_id))
    
    # Add export metadata
    report['export_format'] = 'json'
    report['exported_at'] = str(uuid.uuid4())  # Placeholder for timestamp
    
    return Response(report)
