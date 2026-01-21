import pytest
from unittest.mock import Mock, patch
from domain.models import EmailCampaign, EmailTemplate
from application.services.email_campaign_service import EmailCampaignService, TemplateManagementService, CampaignSchedulingService

@pytest.mark.django_db
class TestEmailCampaignService:
    def test_create_campaign(self):
        """Test creating campaign"""
        service = EmailCampaignService()
        campaign = service.create_campaign({
            'name': 'Test Campaign',
            'subject': 'Test Subject'
        })
        assert campaign.name == 'Test Campaign'

    def test_get_campaigns(self):
        """Test getting campaigns"""
        EmailCampaign.objects.create(name="Campaign 1", subject="Subject 1")
        EmailCampaign.objects.create(name="Campaign 2", subject="Subject 2")
        
        service = EmailCampaignService()
        campaigns = service.get_campaigns()
        assert campaigns.count() == 2

@pytest.mark.django_db
class TestTemplateManagementService:
    def test_create_template(self):
        """Test creating template"""
        service = TemplateManagementService()
        template = service.create_template({
            'name': 'Welcome',
            'content': 'Hello {{name}}'
        })
        assert template.name == 'Welcome'

    def test_get_templates(self):
        """Test getting templates"""
        EmailTemplate.objects.create(name="Template 1", content="Content 1")
        EmailTemplate.objects.create(name="Template 2", content="Content 2")
        
        service = TemplateManagementService()
        templates = service.get_templates()
        assert templates.count() == 2

@pytest.mark.django_db
class TestCampaignSchedulingService:
    @patch('application.services.email_campaign_service.SESEmailService')
    def test_send_campaign(self, mock_ses):
        """Test sending campaign"""
        campaign = EmailCampaign.objects.create(
            name="Test",
            subject="Test",
            content="Hello",
            status='scheduled'
        )
        
        service = CampaignSchedulingService()
        result = service.send_campaign(campaign.id, ['test@example.com'])
        
        assert result is True
        campaign.refresh_from_db()
        assert campaign.status == 'sent'

    def test_schedule_campaign(self):
        """Test scheduling campaign"""
        from django.utils import timezone
        from datetime import timedelta
        
        campaign = EmailCampaign.objects.create(name="Test", subject="Test", status='draft')
        scheduled_time = timezone.now() + timedelta(hours=1)
        
        service = CampaignSchedulingService()
        service.schedule_campaign(campaign.id, scheduled_time)
        
        campaign.refresh_from_db()
        assert campaign.status == 'scheduled'
        assert campaign.scheduled_at == scheduled_time
