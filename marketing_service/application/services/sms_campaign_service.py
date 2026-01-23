from domain.models import SMSCampaign, SMSTemplate
from infrastructure.sms.twilio_service import TwilioSMSService

class SMSCampaignService:
    def create_campaign(self, data):
        return SMSCampaign.objects.create(**data)

    def get_campaigns(self):
        return SMSCampaign.objects.all()

    def get_campaign(self, campaign_id):
        return SMSCampaign.objects.get(id=campaign_id)

class SMSSchedulingService:
    def schedule_campaign(self, campaign_id, scheduled_time):
        campaign = SMSCampaign.objects.get(id=campaign_id)
        campaign.scheduled_at = scheduled_time
        campaign.schedule()
        return campaign

class SMSDeliveryService:
    def __init__(self):
        try:
            self.sms_service = TwilioSMSService()
        except Exception:
            self.sms_service = None

    def send_campaign(self, campaign_id, phone_numbers):
        campaign = SMSCampaign.objects.get(id=campaign_id)
        try:
            if self.sms_service:
                for phone in phone_numbers:
                    self.sms_service.send_sms(phone, campaign.message)
            campaign.mark_sent()
            return True
        except Exception:
            campaign.mark_failed()
            return False
