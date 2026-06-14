from rest_framework import serializers
from .models import InsuranceCompany, InsurancePolicy, PolicyClause


class InsuranceCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceCompany
        fields = '__all__'


class PolicyClauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyClause
        fields = '__all__'


class InsurancePolicySerializer(serializers.ModelSerializer):
    clauses = PolicyClauseSerializer(many=True, read_only=True)

    class Meta:
        model = InsurancePolicy
        fields = '__all__'