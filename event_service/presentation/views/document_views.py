import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from application.document_service import (
    DocumentManagementService,
    DocumentUploadService,
    DocumentAccessService,
)
from infrastructure.services.s3_document_service import S3DocumentService
from domain.document import Document
from presentation.serializers.document_serializers import (
    DocumentSerializer,
    UploadDocumentSerializer,
)


@api_view(['POST'])
def upload_document(request, event_id):
    """Generate presigned URL for document upload."""
    serializer = UploadDocumentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        event_uuid = uuid.UUID(event_id)
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Validate upload
    upload_service = DocumentUploadService()
    try:
        upload_service.validate_upload(
            serializer.validated_data['mime_type'],
            serializer.validated_data['file_size']
        )
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # Generate upload URL
    s3_service = S3DocumentService()
    upload_data = s3_service.generate_upload_url(
        event_uuid,
        serializer.validated_data['file_name'],
        serializer.validated_data['mime_type']
    )
    
    # Create document record
    doc_service = DocumentManagementService()
    doc = doc_service.create_document({
        'event_id': event_uuid,
        'title': serializer.validated_data['title'],
        'description': serializer.validated_data.get('description', ''),
        'document_type': serializer.validated_data['document_type'],
        'file_name': serializer.validated_data['file_name'],
        'file_size': serializer.validated_data['file_size'],
        'mime_type': serializer.validated_data['mime_type'],
        's3_key': upload_data['s3_key'],
        'access_level': serializer.validated_data.get('access_level', 'public'),
        'is_required': serializer.validated_data.get('is_required', False),
        'created_by': serializer.validated_data['created_by'],
    })
    
    return Response({
        'upload_url': upload_data['upload_url'],
        'document_id': str(doc.id),
        'download_url': upload_data['download_url'],
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_documents(request, event_id):
    """Get documents for event."""
    try:
        event_uuid = uuid.UUID(event_id)
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    user_role = request.GET.get('role', 'guest')
    
    access_service = DocumentAccessService()
    docs = access_service.get_accessible_documents(event_uuid, user_role)
    
    return Response(DocumentSerializer(docs, many=True).data)


@api_view(['GET'])
def download_document(request, event_id, document_id):
    """Get presigned URL for document download."""
    try:
        doc_uuid = uuid.UUID(document_id)
    except ValueError:
        return Response({'error': 'Invalid document ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    user_role = request.GET.get('role', 'guest')
    
    try:
        doc_service = DocumentManagementService()
        doc = doc_service.get_document(doc_uuid, user_role)
        
        s3_service = S3DocumentService()
        download_url = s3_service.generate_download_url(doc.s3_key)
        
        doc.increment_downloads()
        
        return Response({
            'download_url': download_url,
            'file_name': doc.file_name,
            'file_size': doc.file_size,
        })
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


@api_view(['DELETE'])
def delete_document(request, event_id, document_id):
    """Delete document."""
    try:
        doc_uuid = uuid.UUID(document_id)
    except ValueError:
        return Response({'error': 'Invalid document ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        doc = Document.objects.get(id=doc_uuid)
        s3_service = S3DocumentService()
        s3_service.delete_file(doc.s3_key)
        
        doc_service = DocumentManagementService()
        doc_service.delete_document(doc_uuid)
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Document.DoesNotExist:
        return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
