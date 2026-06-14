from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Patient, Claim
from .serializers import PatientSerializer, ClaimSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class ClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all().order_by('-created_at')
    serializer_class = ClaimSerializer

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        claim = self.get_object()

        approved_amount = claim.calculate_approved_amount()

        if approved_amount == 0:
            claim.status = 'REJECTED'
            claim.decision_reason = 'Claim amount is not payable based on policy limit and deductible.'
        elif approved_amount < claim.claimed_amount:
            claim.status = 'PARTIALLY_APPROVED'
            claim.decision_reason = 'Claim partially approved due to policy limit or deductible.'
        else:
            claim.status = 'APPROVED'
            claim.decision_reason = 'Claim approved successfully.'

        claim.save()

        serializer = self.get_serializer(claim)

        return Response({
            'message': 'Claim processed successfully',
            'claim': serializer.data
        })