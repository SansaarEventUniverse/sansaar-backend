from typing import Dict, Any
import uuid
import json
from django.core.cache import cache

from domain.registration_form import RegistrationForm


class FormDataStorageService:
    """Service for storing and retrieving form submission data."""
    
    def store_submission(self, form_id: uuid.UUID, user_id: uuid.UUID, 
                        data: Dict[str, Any]) -> str:
        """Store form submission data."""
        submission_id = str(uuid.uuid4())
        key = f"form_submission:{submission_id}"
        
        submission = {
            'form_id': str(form_id),
            'user_id': str(user_id),
            'data': data,
        }
        
        cache.set(key, json.dumps(submission), timeout=86400)  # 24 hours
        return submission_id
    
    def get_submission(self, submission_id: str) -> Dict[str, Any]:
        """Retrieve form submission data."""
        key = f"form_submission:{submission_id}"
        data = cache.get(key)
        
        if data:
            return json.loads(data)
        return None
