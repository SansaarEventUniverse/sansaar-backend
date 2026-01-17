from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from application.services.resource_service import ResourceSharingService, LibraryManagementService, ResourceSearchService
from infrastructure.repositories.resource_repository import ResourceRepository
from presentation.serializers.resource_serializers import ResourceLibrarySerializer, SharedResourceSerializer

@api_view(['POST'])
def upload_resource(request):
    """Upload a new resource"""
    serializer = SharedResourceSerializer(data=request.data)
    if serializer.is_valid():
        service = ResourceSharingService()
        resource = service.upload_resource(serializer.validated_data)
        return Response(SharedResourceSerializer(resource).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def search_resources(request):
    """Search resources by query, tags, or category"""
    query = request.query_params.get('q')
    tags = request.query_params.getlist('tags')
    category = request.query_params.get('category')
    
    service = ResourceSearchService()
    
    if query:
        resources = service.search_by_title(query)
    elif tags:
        resources = service.search_by_tags(tags)
    elif category:
        resources = service.search_by_category(category)
    else:
        resources = []
    
    serializer = SharedResourceSerializer(resources, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_resource_library(request):
    """Get all public libraries"""
    service = LibraryManagementService()
    libraries = service.get_all_libraries()
    serializer = ResourceLibrarySerializer(libraries, many=True)
    return Response(serializer.data)
