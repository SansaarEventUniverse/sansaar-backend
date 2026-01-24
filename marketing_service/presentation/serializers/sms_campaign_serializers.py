from rest_framework import serializers
from domain.models import SMSCampaign

class SMSCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSCampaign
        fields = '__all__'

class SendSMSSerializer(serializers.Serializer):
    phone_numbers = serializers.ListField(child=serializers.CharField())
