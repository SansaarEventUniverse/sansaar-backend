import uuid
from django.test import TestCase

from infrastructure.services.form_storage_service import FormDataStorageService


class FormDataStorageServiceTest(TestCase):
    """Tests for FormDataStorageService."""
    
    def test_store_and_retrieve_submission(self):
        """Test storing and retrieving form submission."""
        service = FormDataStorageService()
        form_id = uuid.uuid4()
        user_id = uuid.uuid4()
        data = {'Full Name': 'John Doe', 'Email': 'john@example.com'}
        
        submission_id = service.store_submission(form_id, user_id, data)
        
        retrieved = service.get_submission(submission_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved['data']['Full Name'], 'John Doe')
