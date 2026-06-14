from rest_framework import serializers
from .models import ClaimDocument, OCRResult


class ClaimDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimDocument
        fields = '__all__'


class OCRResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCRResult
        fields = '__all__'