from rest_framework import viewsets
from .models import InsuranceCompany, InsurancePolicy, PolicyClause
from .serializers import (
    InsuranceCompanySerializer,
    InsurancePolicySerializer,
    PolicyClauseSerializer
)


class InsuranceCompanyViewSet(viewsets.ModelViewSet):
    queryset = InsuranceCompany.objects.all()
    serializer_class = InsuranceCompanySerializer


class InsurancePolicyViewSet(viewsets.ModelViewSet):
    queryset = InsurancePolicy.objects.all()
    serializer_class = InsurancePolicySerializer


class PolicyClauseViewSet(viewsets.ModelViewSet):
    queryset = PolicyClause.objects.all()
    serializer_class = PolicyClauseSerializer