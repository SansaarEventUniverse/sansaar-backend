from typing import Dict, Any, List
import uuid
from datetime import date, timedelta
from django.db.models import Count, Avg

from domain.search_analytics import SearchQuery, SearchAnalytics


class SearchAnalyticsService:
    """Service for search analytics."""
    
    def track_search(self, query_text: str, result_count: int, 
                    response_time_ms: int, filters: Dict = None,
                    user_id: uuid.UUID = None) -> SearchQuery:
        """Track a search query."""
        return SearchQuery.objects.create(
            query_text=query_text,
            result_count=result_count,
            response_time_ms=response_time_ms,
            filters=filters or {},
            user_id=user_id,
        )
    
    def get_analytics(self, days: int = 7) -> Dict[str, Any]:
        """Get search analytics for last N days."""
        start_date = date.today() - timedelta(days=days)
        queries = SearchQuery.objects.filter(created_at__date__gte=start_date)
        
        total_searches = queries.count()
        unique_queries = queries.values('query_text').distinct().count()
        avg_response = queries.aggregate(Avg('response_time_ms'))['response_time_ms__avg'] or 0
        
        # Popular queries
        popular = list(
            queries.values('query_text')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )
        
        # Zero result queries
        zero_results = list(
            queries.filter(result_count=0)
            .values_list('query_text', flat=True)
            .distinct()[:10]
        )
        
        return {
            'total_searches': total_searches,
            'unique_queries': unique_queries,
            'avg_response_time_ms': round(avg_response, 2),
            'popular_queries': popular,
            'zero_result_queries': list(zero_results),
        }


class QueryAnalysisService:
    """Service for analyzing search queries."""
    
    def get_popular_searches(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most popular search queries."""
        queries = (
            SearchQuery.objects
            .values('query_text')
            .annotate(count=Count('id'))
            .order_by('-count')[:limit]
        )
        return list(queries)
    
    def get_zero_result_queries(self, limit: int = 10) -> List[str]:
        """Get queries that returned zero results."""
        queries = (
            SearchQuery.objects
            .filter(result_count=0)
            .values_list('query_text', flat=True)
            .distinct()[:limit]
        )
        return list(queries)


class SearchOptimizationService:
    """Service for search optimization insights."""
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get search performance metrics."""
        queries = SearchQuery.objects.all()
        
        if not queries.exists():
            return {
                'avg_response_time': 0,
                'slow_queries': [],
                'fast_queries': [],
            }
        
        avg_time = queries.aggregate(Avg('response_time_ms'))['response_time_ms__avg']
        
        # Slow queries (> 500ms)
        slow = list(
            queries.filter(response_time_ms__gt=500)
            .values('query_text', 'response_time_ms')
            .order_by('-response_time_ms')[:5]
        )
        
        # Fast queries (< 100ms)
        fast = list(
            queries.filter(response_time_ms__lt=100)
            .values('query_text', 'response_time_ms')
            .order_by('response_time_ms')[:5]
        )
        
        return {
            'avg_response_time': round(avg_time, 2),
            'slow_queries': slow,
            'fast_queries': fast,
        }
