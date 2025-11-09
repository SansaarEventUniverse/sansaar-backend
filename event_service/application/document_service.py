import uuid
from typing import Dict, List, Optional
from django.core.exceptions import ValidationError

from domain.document import Document


class DocumentUploadService:
    """Service for document upload validation."""
    
    ALLOWED_MIME_TYPES = {
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'text/plain',
    }
    
    def validate_upload(self, mime_type: str, file_size: int) -> None:
        """Validate document upload."""
        if mime_type not in self.ALLOWED_MIME_TYPES:
            raise ValidationError(f"File type {mime_type} not allowed")
        
        MAX_SIZE = 100 * 1024 * 1024
        if file_size > MAX_SIZE:
            raise ValidationError(f"File size exceeds maximum of {MAX_SIZE} bytes")


class DocumentAccessService:
    """Service for document access control."""
    
    def check_access(self, document: Document, user_id: uuid.UUID, user_role: str) -> bool:
        """Check if user can access document."""
        return document.can_access(user_role)
    
    def get_accessible_documents(
        self, event_id: uuid.UUID, user_role: str
    ) -> List[Document]:
        """Get documents accessible to user."""
        all_docs = Document.objects.filter(event_id=event_id).order_by('-created_at')
        return [doc for doc in all_docs if doc.can_access(user_role)]


class DocumentVersioningService:
    """Service for document versioning."""
    
    def create_version(
        self, document_id: uuid.UUID, new_s3_key: str, new_file_size: int
    ) -> Document:
        """Create new version of document."""
        try:
            doc = Document.objects.get(id=document_id)
            return doc.create_new_version(new_s3_key, new_file_size)
        except Document.DoesNotExist:
            raise ValidationError("Document not found")
    
    def get_version_history(self, document_id: uuid.UUID) -> List[Document]:
        """Get version history of document."""
        versions = []
        try:
            current = Document.objects.get(id=document_id)
            versions.append(current)
            
            while current.previous_version_id:
                current = Document.objects.get(id=current.previous_version_id)
                versions.append(current)
        except Document.DoesNotExist:
            pass
        
        return versions


class DocumentManagementService:
    """Service for document management."""
    
    def __init__(self):
        self.upload_service = DocumentUploadService()
        self.access_service = DocumentAccessService()
        self.versioning_service = DocumentVersioningService()
    
    def create_document(self, data: Dict) -> Document:
        """Create new document."""
        doc = Document.objects.create(**data)
        doc.validate_file_size()
        return doc
    
    def get_document(self, document_id: uuid.UUID, user_role: str) -> Optional[Document]:
        """Get document if user has access."""
        try:
            doc = Document.objects.get(id=document_id)
            if self.access_service.check_access(doc, None, user_role):
                return doc
            raise ValidationError("Access denied")
        except Document.DoesNotExist:
            raise ValidationError("Document not found")
    
    def delete_document(self, document_id: uuid.UUID) -> None:
        """Delete document."""
        try:
            doc = Document.objects.get(id=document_id)
            doc.delete()
        except Document.DoesNotExist:
            raise ValidationError("Document not found")
