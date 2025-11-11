import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from application.template_service import (
    CreateTemplateService,
    ApplyTemplateService,
    TemplateManagementService,
)
from presentation.serializers.template_serializers import (
    EventTemplateSerializer,
    CreateTemplateSerializer,
    ApplyTemplateSerializer,
)


@api_view(['POST'])
def create_template(request):
    """Create new event template."""
    serializer = CreateTemplateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = CreateTemplateService()
        template = service.create_custom(serializer.validated_data)
        
        return Response(
            EventTemplateSerializer(template).data,
            status=status.HTTP_201_CREATED
        )
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_templates(request):
    """Get event templates."""
    user_id = request.GET.get('user_id')
    org_id = request.GET.get('organization_id')
    category = request.GET.get('category')
    featured = request.GET.get('featured')
    
    if not user_id:
        return Response({'error': 'user_id required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user_uuid = uuid.UUID(user_id)
        org_uuid = uuid.UUID(org_id) if org_id else None
    except ValueError:
        return Response({'error': 'Invalid UUID'}, status=status.HTTP_400_BAD_REQUEST)
    
    service = TemplateManagementService()
    
    if featured:
        templates = service.get_featured_templates()
    else:
        templates = service.get_templates(user_uuid, org_uuid, category)
    
    return Response(EventTemplateSerializer(templates, many=True).data)


@api_view(['GET'])
def get_template(request, template_id):
    """Get single template."""
    try:
        template_uuid = uuid.UUID(template_id)
    except ValueError:
        return Response({'error': 'Invalid template ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    from domain.template import EventTemplate
    try:
        template = EventTemplate.objects.get(id=template_uuid)
        return Response(EventTemplateSerializer(template).data)
    except EventTemplate.DoesNotExist:
        return Response({'error': 'Template not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def apply_template(request, event_id):
    """Apply template to event."""
    serializer = ApplyTemplateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = ApplyTemplateService()
        merged_data = service.apply_to_event(
            serializer.validated_data['template_id'],
            serializer.validated_data['event_data'],
            serializer.validated_data['user_id']
        )
        
        return Response({'event_data': merged_data}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_template(request, template_id):
    """Update template."""
    try:
        template_uuid = uuid.UUID(template_id)
    except ValueError:
        return Response({'error': 'Invalid template ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    user_id = request.data.get('user_id')
    if not user_id:
        return Response({'error': 'user_id required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        return Response({'error': 'Invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = TemplateManagementService()
        template = service.update_template(template_uuid, request.data, user_uuid)
        
        return Response(EventTemplateSerializer(template).data)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_template(request, template_id):
    """Delete template."""
    try:
        template_uuid = uuid.UUID(template_id)
    except ValueError:
        return Response({'error': 'Invalid template ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    user_id = request.GET.get('user_id')
    if not user_id:
        return Response({'error': 'user_id required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        return Response({'error': 'Invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = TemplateManagementService()
        service.delete_template(template_uuid, user_uuid)
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def clone_template(request, template_id):
    """Clone template."""
    try:
        template_uuid = uuid.UUID(template_id)
    except ValueError:
        return Response({'error': 'Invalid template ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    user_id = request.data.get('user_id')
    new_name = request.data.get('name')
    
    if not user_id:
        return Response({'error': 'user_id required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        return Response({'error': 'Invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = TemplateManagementService()
        cloned = service.clone_template(template_uuid, user_uuid, new_name)
        
        return Response(
            EventTemplateSerializer(cloned).data,
            status=status.HTTP_201_CREATED
        )
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
