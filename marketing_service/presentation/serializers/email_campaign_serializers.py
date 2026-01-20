from rest_framework import serializers
from domain.models import EmailCampaign, EmailTemplate

class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = ['id', 'name', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class EmailCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailCampaign
        fields = ['id', 'name', 'subject', 'template', 'content', 'status', 'scheduled_at', 'sent_at', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'sent_at', 'created_at', 'updated_at']
