from rest_framework import serializers
from domain.models import MentorshipProgram, MentorMentee

class MentorshipProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorshipProgram
        fields = ['id', 'title', 'description', 'skills_required', 'duration_weeks', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class MentorMenteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorMentee
        fields = ['id', 'program', 'mentor_user_id', 'mentee_user_id', 'status', 'start_date', 'end_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
