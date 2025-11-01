from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from application.search_service import (
    EventSearchService,
    SearchFilterService,
)
from infrastructure.services.search_cache_service import SearchCacheService
from presentation.serializers.search_serializers import (
    EventSearchResultSerializer,
    SearchFiltersSerializer,
)


@api_view(['GET'])
def search_events(request):
    """Search events with query and filters."""
    query = request.GET.get('q', '')
    category = request.GET.get('category')
    city = request.GET.get('city')
    
    filters = {}
    if category:
        filters['category'] = category
    if city:
        filters['city'] = city
    
    # Check cache first
    cache_service = SearchCacheService()
    cached = cache_service.get_cached_results(query, filters)
    
    if cached:
        return Response({
            'results': cached,
            'count': len(cached),
            'cached': True
        })
    
    # Perform search
    search_service = EventSearchService()
    results = search_service.execute(query, filters)
    
    # Cache results
    cache_service.cache_results(query, filters, results)
    
    serializer = EventSearchResultSerializer(results, many=True)
    return Response({
        'results': serializer.data,
        'count': len(results),
        'cached': False
    })


@api_view(['GET'])
def get_search_filters(request):
    """Get available search filters."""
    service = SearchFilterService()
    filters = service.execute()
    
    serializer = SearchFiltersSerializer(filters)
    return Response(serializer.data)


@api_view(['GET'])
def get_search_suggestions(request):
    """Get search suggestions based on query."""
    query = request.GET.get('q', '')
    
    if not query or len(query) < 2:
        return Response({'suggestions': []})
    
    # Get top 5 matching titles
    search_service = EventSearchService()
    results = search_service.execute(query)[:5]
    
    suggestions = [
        {
            'event_id': str(r.event_id),
            'title': r.title,
            'category': r.category,
        }
        for r in results
    ]
    
    return Response({'suggestions': suggestions})
