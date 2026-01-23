import pytest
from domain.models import SMSCampaign, SMSTemplate
from application.services.sms_campaign_service import SMSCampaignService, SMSSchedulingService, SMSDeliveryService

@pytest.mark.django_db
class TestSMSCampaignService:
    def test_create_campaign(self):
        """Test creating SMS campaign"""
        service = SMSCampaignService()
        campaign = service.create_campaign({
            'name': 'Test SMS',
            'message': 'Test Message'
        })
        assert campaign.name == 'Test SMS'

    def test_get_campaigns(self):
        """Test getting campaigns"""
        SMSCampaign.objects.create(name="Campaign 1", message="Message 1")
        SMSCampaign.objects.create(name="Campaign 2", message="Message 2")
        
        service = SMSCampaignService()
        campaigns = service.get_campaigns()
        assert campaigns.count() == 2

@pytest.mark.django_db
class TestSMSSchedulingService:
    def test_schedule_campaign(self):
        """Test scheduling SMS campaign"""
        from django.utils import timezone
        from datetime import timedelta
        
        campaign = SMSCampaign.objects.create(name="Test", message="Test", status='draft')
        scheduled_time = timezone.now() + timedelta(hours=1)
        
        service = SMSSchedulingService()
        service.schedule_campaign(campaign.id, scheduled_time)
        
        campaign.refresh_from_db()
        assert campaign.status == 'scheduled'
        assert campaign.scheduled_at == scheduled_time

@pytest.mark.django_db
class TestSMSDeliveryService:
    def test_send_sms(self):
        """Test sending SMS"""
        campaign = SMSCampaign.objects.create(
            name="Test",
            message="Hello",
            status='scheduled'
        )
        
        service = SMSDeliveryService()
        result = service.send_campaign(campaign.id, ['+1234567890'])
        
        campaign.refresh_from_db()
        assert campaign.status in ['sent', 'failed']
