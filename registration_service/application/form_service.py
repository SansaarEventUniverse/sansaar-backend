from typing import Dict, Any, List
import uuid
from django.core.exceptions import ValidationError

from domain.registration_form import RegistrationForm, CustomField


class CreateRegistrationFormService:
    """Service for creating registration forms."""
    
    def execute(self, event_id: uuid.UUID, title: str, 
                fields: List[Dict[str, Any]]) -> RegistrationForm:
        """Create a registration form with custom fields."""
        form = RegistrationForm.objects.create(
            event_id=event_id,
            title=title,
        )
        
        for field_data in fields:
            field = CustomField(
                form=form,
                label=field_data['label'],
                field_type=field_data['field_type'],
                is_required=field_data.get('is_required', False),
                order=field_data.get('order', 0),
                options=field_data.get('options'),
            )
            field.clean()
            field.save()
        
        return form


class ValidateRegistrationDataService:
    """Service for validating registration form data."""
    
    def execute(self, form_id: uuid.UUID, data: Dict[str, Any]) -> bool:
        """Validate form submission data."""
        try:
            form = RegistrationForm.objects.get(id=form_id)
        except RegistrationForm.DoesNotExist:
            raise ValidationError('Form not found')
        
        fields = form.fields.all()
        errors = {}
        
        for field in fields:
            field_value = data.get(field.label)
            
            if field.is_required and not field_value:
                errors[field.label] = 'This field is required'
            
            if field_value and field.field_type == 'email':
                if '@' not in str(field_value):
                    errors[field.label] = 'Invalid email format'
        
        if errors:
            raise ValidationError(errors)
        
        return True


class GetRegistrationFormService:
    """Service for retrieving registration forms."""
    
    def execute(self, event_id: uuid.UUID) -> RegistrationForm:
        """Get registration form for an event."""
        try:
            return RegistrationForm.objects.prefetch_related('fields').get(
                event_id=event_id
            )
        except RegistrationForm.DoesNotExist:
            raise ValidationError('Form not found for event')
