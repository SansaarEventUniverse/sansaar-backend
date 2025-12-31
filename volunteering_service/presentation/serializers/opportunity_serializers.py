from rest_framework import serializers
from domain.models import VolunteerOpportunity, VolunteerSkill

class VolunteerSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerSkill
        fields = ['id', 'skill_name', 'proficiency_level', 'is_required']

class VolunteerOpportunitySerializer(serializers.ModelSerializer):
    skills = VolunteerSkillSerializer(many=True, required=False)
    
    class Meta:
        model = VolunteerOpportunity
        fields = ['id', 'title', 'description', 'location', 'start_date', 'end_date', 
                  'volunteers_needed', 'volunteers_registered', 'status', 'skills', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        skills_data = validated_data.pop('skills', [])
        opportunity = VolunteerOpportunity.objects.create(**validated_data)
        for skill_data in skills_data:
            VolunteerSkill.objects.create(opportunity=opportunity, **skill_data)
        return opportunity
    
    def update(self, instance, validated_data):
        skills_data = validated_data.pop('skills', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if skills_data is not None:
            instance.skills.all().delete()
            for skill_data in skills_data:
                VolunteerSkill.objects.create(opportunity=instance, **skill_data)
        
        return instance
