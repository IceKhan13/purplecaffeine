# Serializer Module to convert complex data types such as Django model instances into native Python data types 
from rest_framework import serializers
from .models import Trial


class TrialSerializer(serializers.ModelSerializer):
    # Serializer class for Trial model
    class Meta:
        # defines the metadata for the serializer and specifies the model 
        model = Trial
        fields = "__all__"
