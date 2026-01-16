from rest_framework import serializers
from domain.models import EventCollaboration, CollaborationTask

class EventCollaborationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCollaboration
        fields = ['id', 'event_id', 'name', 'description', 'team_members', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class CollaborationTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollaborationTask
        fields = ['id', 'collaboration', 'title', 'description', 'assigned_to', 'status', 'priority', 'due_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
