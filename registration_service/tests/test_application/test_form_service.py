import uuid
from django.test import TestCase
from django.core.exceptions import ValidationError

from domain.registration_form import RegistrationForm
from application.form_service import (
    CreateRegistrationFormService,
    ValidateRegistrationDataService,
    GetRegistrationFormService,
)


class CreateRegistrationFormServiceTest(TestCase):
    """Tests for CreateRegistrationFormService."""
    
    def test_create_form_with_fields(self):
        """Test creating form with custom fields."""
        service = CreateRegistrationFormService()
        event_id = uuid.uuid4()
        
        fields = [
            {'label': 'Full Name', 'field_type': 'text', 'is_required': True, 'order': 1},
            {'label': 'Email', 'field_type': 'email', 'is_required': True, 'order': 2},
        ]
        
        form = service.execute(event_id, 'Registration', fields)
        
        self.assertIsNotNone(form.id)
        self.assertEqual(form.fields.count(), 2)


class ValidateRegistrationDataServiceTest(TestCase):
    """Tests for ValidateRegistrationDataService."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
        self.form = RegistrationForm.objects.create(
            event_id=self.event_id,
            title='Registration',
        )
        
    def test_validate_required_fields(self):
        """Test validation of required fields."""
        from domain.registration_form import CustomField
        CustomField.objects.create(
            form=self.form,
            label='Full Name',
            field_type='text',
            is_required=True,
            order=1,
        )
        
        service = ValidateRegistrationDataService()
        
        with self.assertRaises(ValidationError):
            service.execute(self.form.id, {})


class GetRegistrationFormServiceTest(TestCase):
    """Tests for GetRegistrationFormService."""
    
    def test_get_form_by_event(self):
        """Test retrieving form by event ID."""
        event_id = uuid.uuid4()
        form = RegistrationForm.objects.create(
            event_id=event_id,
            title='Registration',
        )
        
        service = GetRegistrationFormService()
        retrieved = service.execute(event_id)
        
        self.assertEqual(retrieved.id, form.id)
