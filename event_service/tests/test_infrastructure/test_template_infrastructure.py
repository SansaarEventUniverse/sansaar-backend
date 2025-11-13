import uuid
from django.test import TestCase

from infrastructure.services.template_infrastructure_service import (
    TemplateStorageService,
    TemplateMarketplaceService,
    TemplateAnalyticsService,
    TemplateValidationService,
)


class TemplateStorageServiceTest(TestCase):
    """Tests for TemplateStorageService."""
    
    def test_store_template(self):
        """Test storing template."""
        service = TemplateStorageService()
        result = service.store_template(uuid.uuid4(), {'title': 'Test'})
        
        self.assertTrue(result)
        
    def test_retrieve_template(self):
        """Test retrieving template."""
        service = TemplateStorageService()
        data = service.retrieve_template(uuid.uuid4())
        
        self.assertIsInstance(data, dict)


class TemplateMarketplaceServiceTest(TestCase):
    """Tests for TemplateMarketplaceService."""
    
    def test_publish_to_marketplace(self):
        """Test publishing to marketplace."""
        service = TemplateMarketplaceService()
        result = service.publish_to_marketplace(uuid.uuid4())
        
        self.assertTrue(result)
        
    def test_get_marketplace_templates(self):
        """Test getting marketplace templates."""
        service = TemplateMarketplaceService()
        templates = service.get_marketplace_templates('conference')
        
        self.assertIsInstance(templates, list)
        
    def test_rate_template(self):
        """Test rating template."""
        service = TemplateMarketplaceService()
        result = service.rate_template(uuid.uuid4(), uuid.uuid4(), 5)
        
        self.assertTrue(result)


class TemplateAnalyticsServiceTest(TestCase):
    """Tests for TemplateAnalyticsService."""
    
    def test_get_usage_stats(self):
        """Test getting usage statistics."""
        service = TemplateAnalyticsService()
        stats = service.get_usage_stats(uuid.uuid4())
        
        self.assertIn('total_uses', stats)
        self.assertIn('unique_users', stats)
        
    def test_get_popular_templates(self):
        """Test getting popular templates."""
        service = TemplateAnalyticsService()
        popular = service.get_popular_templates(5)
        
        self.assertIsInstance(popular, list)


class TemplateValidationServiceTest(TestCase):
    """Tests for TemplateValidationService."""
    
    def test_validate_structure(self):
        """Test validating template structure."""
        service = TemplateValidationService()
        
        valid = service.validate_structure({
            'title': 'Event',
            'description': 'Description',
        })
        self.assertTrue(valid)
        
        invalid = service.validate_structure({'title': 'Event'})
        self.assertFalse(invalid)
        
    def test_sanitize_data(self):
        """Test sanitizing template data."""
        service = TemplateValidationService()
        data = {
            'title': 'Event',
            'description': 'Test',
            'password': 'secret123',
            'api_key': 'key123',
        }
        
        sanitized = service.sanitize_data(data)
        
        self.assertIn('title', sanitized)
        self.assertNotIn('password', sanitized)
        self.assertNotIn('api_key', sanitized)
