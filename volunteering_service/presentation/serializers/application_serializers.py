from rest_framework import serializers
from domain.models import VolunteerApplication

class VolunteerApplicationSerializer(serializers.ModelSerializer):
    opportunity_title = serializers.CharField(source='opportunity.title', read_only=True)
    
    class Meta:
        model = VolunteerApplication
        fields = ['id', 'opportunity', 'opportunity_title', 'volunteer_name', 
                  'volunteer_email', 'volunteer_phone', 'status', 'applied_at', 'updated_at']
        read_only_fields = ['id', 'applied_at', 'updated_at']
