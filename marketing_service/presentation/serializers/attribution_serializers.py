from rest_framework import serializers
from domain.models import AttributionModel, TouchPoint

class AttributionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributionModel
        fields = '__all__'

class TouchPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = TouchPoint
        fields = '__all__'
