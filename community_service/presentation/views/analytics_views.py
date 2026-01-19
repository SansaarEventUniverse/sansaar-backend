from rest_framework.decorators import api_view
from rest_framework.response import Response
from application.services.analytics_service import CommunityAnalyticsService, InsightsGenerationService
from infrastructure.repositories.analytics_repository import AnalyticsRepository
from presentation.serializers.analytics_serializers import CommunityAnalyticsSerializer, EngagementMetricsSerializer

@api_view(['GET'])
def get_community_analytics(request):
    """Get community analytics"""
    metric_type = request.query_params.get('type')
    
    service = CommunityAnalyticsService()
    if metric_type:
        analytics = service.get_analytics_by_type(metric_type)
    else:
        analytics = []
    
    serializer = CommunityAnalyticsSerializer(analytics, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_engagement_report(request):
    """Get engagement report"""
    try:
        days = int(request.query_params.get('days', 7))
        if days <= 0:
            days = 7
    except (ValueError, TypeError):
        days = 7
    
    repo = AnalyticsRepository()
    trends = repo.get_engagement_trends(days=days)
    active_users = repo.get_active_users_count(days=days)
    
    return Response({
        'trends': trends,
        'active_users': active_users,
        'period_days': days
    })

@api_view(['GET'])
def get_insights_dashboard(request):
    """Get insights dashboard"""
    service = InsightsGenerationService()
    
    top_users = service.generate_top_users(limit=10)
    summary = service.generate_engagement_summary()
    
    return Response({
        'top_users': EngagementMetricsSerializer(top_users, many=True).data,
        'summary': summary
    })
