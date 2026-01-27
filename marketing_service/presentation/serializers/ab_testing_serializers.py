from rest_framework import serializers
from domain.models import ABTest, TestVariant

class ABTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ABTest
        fields = '__all__'

class TestVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestVariant
        fields = '__all__'
