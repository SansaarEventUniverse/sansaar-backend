import uuid
from django.test import TestCase
from django.core.exceptions import ValidationError

from domain.registration_form import RegistrationForm, CustomField


class RegistrationFormModelTest(TestCase):
    """Tests for RegistrationForm model."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
        
    def test_create_form(self):
        """Test creating a registration form."""
        form = RegistrationForm.objects.create(
            event_id=self.event_id,
            title='Event Registration',
        )
        self.assertIsNotNone(form.id)
        self.assertTrue(form.is_active)


class CustomFieldModelTest(TestCase):
    """Tests for CustomField model."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
        self.form = RegistrationForm.objects.create(
            event_id=self.event_id,
            title='Event Registration',
        )
        
    def test_create_custom_field(self):
        """Test creating a custom field."""
        field = CustomField.objects.create(
            form=self.form,
            label='Full Name',
            field_type='text',
            is_required=True,
            order=1,
        )
        self.assertIsNotNone(field.id)
        
    def test_select_field_requires_options(self):
        """Test select field validation."""
        field = CustomField(
            form=self.form,
            label='Country',
            field_type='select',
            order=1,
        )
        with self.assertRaises(ValidationError):
            field.clean()
