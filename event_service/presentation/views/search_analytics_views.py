from rest_framework.decorators import api_view
from rest_framework.response import Response

from application.search_analytics_service import (
    SearchAnalyticsService,
    QueryAnalysisService,
    SearchOptimizationService,
)


@api_view(['GET'])
def get_search_analytics(request):
    """Get search analytics."""
    days = int(request.GET.get('days', 7))
    
    service = SearchAnalyticsService()
    analytics = service.get_analytics(days=days)
    
    return Response(analytics)


@api_view(['GET'])
def get_search_performance(request):
    """Get search performance metrics."""
    service = SearchOptimizationService()
    metrics = service.get_performance_metrics()
    
    return Response(metrics)


@api_view(['GET'])
def get_popular_searches(request):
    """Get popular search queries."""
    limit = int(request.GET.get('limit', 10))
    
    service = QueryAnalysisService()
    popular = service.get_popular_searches(limit=limit)
    
    return Response({
        'popular_searches': popular,
        'count': len(popular)
    })
