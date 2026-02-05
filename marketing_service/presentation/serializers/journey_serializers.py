from rest_framework import serializers
from domain.models import CustomerJourney, JourneyStage

class CustomerJourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerJourney
        fields = '__all__'

class JourneyStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = JourneyStage
        fields = '__all__'
