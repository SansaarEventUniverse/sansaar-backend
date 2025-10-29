import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from application.form_service import (
    CreateRegistrationFormService,
    ValidateRegistrationDataService,
    GetRegistrationFormService,
)
from infrastructure.services.form_storage_service import FormDataStorageService
from presentation.serializers.form_serializers import (
    RegistrationFormSerializer,
    CreateFormSerializer,
    SubmitFormSerializer,
)


@api_view(['POST'])
def create_form(request, event_id):
    """Create registration form for event."""
    serializer = CreateFormSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = CreateRegistrationFormService()
        form = service.execute(
            uuid.UUID(event_id),
            serializer.validated_data['title'],
            serializer.validated_data['fields'],
        )
        return Response(
            RegistrationFormSerializer(form).data,
            status=status.HTTP_201_CREATED
        )
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_form(request, event_id):
    """Get registration form for event."""
    try:
        service = GetRegistrationFormService()
        form = service.execute(uuid.UUID(event_id))
        return Response(RegistrationFormSerializer(form).data)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def submit_form(request, event_id):
    """Submit registration form data."""
    serializer = SubmitFormSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Get form
        form_service = GetRegistrationFormService()
        form = form_service.execute(uuid.UUID(event_id))
        
        # Validate data
        validate_service = ValidateRegistrationDataService()
        validate_service.execute(form.id, serializer.validated_data['data'])
        
        # Store submission
        storage_service = FormDataStorageService()
        user_id = uuid.uuid4()  # TODO: Get from auth
        submission_id = storage_service.store_submission(
            form.id,
            user_id,
            serializer.validated_data['data']
        )
        
        return Response(
            {'submission_id': submission_id},
            status=status.HTTP_201_CREATED
        )
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
