from rest_framework import serializers
from .models import Patient, Claim


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class ClaimSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)
    policy_number = serializers.CharField(source='policy.policy_number', read_only=True)

    class Meta:
        model = Claim
        fields = '__all__'