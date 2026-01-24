import pytest
from domain.models import SMSCampaign, SMSTemplate

@pytest.mark.django_db
class TestSMSCampaign:
    def test_create_campaign(self):
        """Test creating SMS campaign"""
        campaign = SMSCampaign.objects.create(
            name="Welcome SMS",
            message="Welcome to Sansaar!",
            status='draft'
        )
        assert campaign.name == "Welcome SMS"
        assert campaign.status == 'draft'

    def test_campaign_status_choices(self):
        """Test campaign status validation"""
        campaign = SMSCampaign.objects.create(name="Test", message="Test", status='scheduled')
        assert campaign.status in ['draft', 'scheduled', 'sent', 'failed']

    def test_schedule_campaign(self):
        """Test scheduling campaign"""
        campaign = SMSCampaign.objects.create(name="Test", message="Test", status='draft')
        campaign.schedule()
        assert campaign.status == 'scheduled'

    def test_send_campaign(self):
        """Test sending campaign"""
        campaign = SMSCampaign.objects.create(name="Test", message="Test", status='scheduled')
        campaign.mark_sent()
        assert campaign.status == 'sent'

@pytest.mark.django_db
class TestSMSTemplate:
    def test_create_template(self):
        """Test creating SMS template"""
        template = SMSTemplate.objects.create(
            name="Welcome Template",
            message="Hello {{name}}, welcome!"
        )
        assert template.name == "Welcome Template"
        assert "{{name}}" in template.message

    def test_render_template(self):
        """Test template rendering"""
        template = SMSTemplate.objects.create(
            name="Test",
            message="Hello {{name}}"
        )
        rendered = template.render({'name': 'John'})
        assert rendered == "Hello John"
