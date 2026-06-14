from rest_framework import serializers
from .models import HumanReview


class HumanReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='reviewer.username', read_only=True)
    claim_id = serializers.IntegerField(source='claim.id', read_only=True)

    class Meta:
        model = HumanReview
        fields = '__all__'