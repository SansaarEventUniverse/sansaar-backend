from domain.models import EmailCampaign, EmailTemplate
from infrastructure.email.ses_service import SESEmailService

class EmailCampaignService:
    def create_campaign(self, data):
        return EmailCampaign.objects.create(**data)

    def get_campaigns(self):
        return EmailCampaign.objects.all()

    def get_campaign(self, campaign_id):
        return EmailCampaign.objects.get(id=campaign_id)

class TemplateManagementService:
    def create_template(self, data):
        return EmailTemplate.objects.create(**data)

    def get_templates(self):
        return EmailTemplate.objects.all()

    def get_template(self, template_id):
        return EmailTemplate.objects.get(id=template_id)

class CampaignSchedulingService:
    def __init__(self):
        try:
            self.email_service = SESEmailService()
        except Exception:
            self.email_service = None

    def send_campaign(self, campaign_id, recipients):
        campaign = EmailCampaign.objects.get(id=campaign_id)
        try:
            if self.email_service:
                for recipient in recipients:
                    self.email_service.send_email(recipient, campaign.subject, campaign.content)
            campaign.mark_sent()
            return True
        except Exception:
            campaign.mark_failed()
            return False

    def schedule_campaign(self, campaign_id, scheduled_time):
        campaign = EmailCampaign.objects.get(id=campaign_id)
        campaign.scheduled_at = scheduled_time
        campaign.schedule()
        return campaign
