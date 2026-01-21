import pytest
from django.core.exceptions import ValidationError
from domain.models import EmailCampaign, EmailTemplate

@pytest.mark.django_db
class TestEmailCampaign:
    def test_create_campaign(self):
        """Test creating email campaign"""
        campaign = EmailCampaign.objects.create(
            name="Welcome Campaign",
            subject="Welcome to Sansaar",
            status='draft'
        )
        assert campaign.name == "Welcome Campaign"
        assert campaign.status == 'draft'

    def test_campaign_status_choices(self):
        """Test campaign status validation"""
        campaign = EmailCampaign.objects.create(name="Test", subject="Test", status='scheduled')
        assert campaign.status in ['draft', 'scheduled', 'sent', 'failed']

    def test_schedule_campaign(self):
        """Test scheduling campaign"""
        campaign = EmailCampaign.objects.create(name="Test", subject="Test", status='draft')
        campaign.schedule()
        assert campaign.status == 'scheduled'

    def test_send_campaign(self):
        """Test sending campaign"""
        campaign = EmailCampaign.objects.create(name="Test", subject="Test", status='scheduled')
        campaign.mark_sent()
        assert campaign.status == 'sent'

@pytest.mark.django_db
class TestEmailTemplate:
    def test_create_template(self):
        """Test creating email template"""
        template = EmailTemplate.objects.create(
            name="Welcome Template",
            content="<h1>Welcome {{name}}</h1>"
        )
        assert template.name == "Welcome Template"
        assert "{{name}}" in template.content

    def test_render_template(self):
        """Test template rendering"""
        template = EmailTemplate.objects.create(
            name="Test",
            content="Hello {{name}}"
        )
        rendered = template.render({'name': 'John'})
        assert rendered == "Hello John"
