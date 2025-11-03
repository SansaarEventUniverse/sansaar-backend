import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from application.category_service import (
    CategoryManagementService,
    TagManagementService,
)
from infrastructure.services.category_analytics_service import (
    CategoryAnalyticsService,
    TagAnalyticsService,
)
from domain.category import Category, Tag
from presentation.serializers.category_serializers import (
    CategorySerializer,
    CreateCategorySerializer,
    TagSerializer,
    CreateTagSerializer,
)


@api_view(['GET', 'POST'])
def manage_categories(request):
    """Get all categories or create a new one."""
    if request.method == 'GET':
        service = CategoryManagementService()
        tree = service.get_category_tree()
        return Response({'categories': tree})
    
    elif request.method == 'POST':
        serializer = CreateCategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service = CategoryManagementService()
            category = service.create_category(serializer.validated_data)
            return Response(
                CategorySerializer(category).data,
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_category_stats(request):
    """Get category statistics."""
    service = CategoryAnalyticsService()
    stats = service.get_category_stats()
    return Response(stats)


@api_view(['GET', 'POST'])
def manage_tags(request):
    """Get all tags or create a new one."""
    if request.method == 'GET':
        limit = int(request.GET.get('limit', 50))
        service = TagManagementService()
        tags = service.get_popular_tags(limit=limit)
        return Response({
            'tags': TagSerializer(tags, many=True).data
        })
    
    elif request.method == 'POST':
        serializer = CreateTagSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        service = TagManagementService()
        tag = service.create_tag(serializer.validated_data['name'])
        return Response(
            TagSerializer(tag).data,
            status=status.HTTP_201_CREATED
        )


@api_view(['GET'])
def get_tag_suggestions(request):
    """Get tag suggestions based on query."""
    query = request.GET.get('q', '')
    
    if not query or len(query) < 2:
        return Response({'suggestions': []})
    
    service = TagManagementService()
    tags = service.suggest_tags(query, limit=10)
    
    return Response({
        'suggestions': TagSerializer(tags, many=True).data
    })


@api_view(['GET'])
def get_tag_stats(request):
    """Get tag statistics."""
    service = TagAnalyticsService()
    stats = service.get_tag_stats()
    return Response(stats)
