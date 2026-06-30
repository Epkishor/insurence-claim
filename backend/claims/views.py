from decimal import Decimal

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ai_engine.orchestrator.supervisor_agent import SupervisorAgent
from .models import Patient, Claim
from .serializers import PatientSerializer, ClaimSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class ClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        claim = self.get_object()

        approved_amount = claim.calculate_approved_amount()

        if approved_amount == 0:
            claim.status = Claim.Status.REJECTED
            claim.decision_reason = 'Claim amount is not payable based on policy limit and deductible.'
        elif approved_amount < claim.claimed_amount:
            claim.status = Claim.Status.PARTIALLY_APPROVED
            claim.decision_reason = 'Claim partially approved due to policy limit or deductible.'
        else:
            claim.status = Claim.Status.APPROVED
            claim.decision_reason = 'Claim approved successfully.'

        claim.save()

        serializer = self.get_serializer(claim)

        return Response({
            'message': 'Claim processed successfully',
            'claim': serializer.data
        })

    @action(detail=True, methods=['post'], url_path='ai-process')
    def ai_process(self, request, pk=None):
        claim = self.get_object()
        claim_data = self._build_ai_claim_data(claim)

        supervisor = SupervisorAgent()
        ai_result = supervisor.process_claim(claim_data)
        final_decision = ai_result.get('final_decision', {})

        self._save_ai_decision(claim, final_decision)

        serializer = self.get_serializer(claim)

        return Response({
            'message': 'AI claim processing completed successfully',
            'claim': serializer.data,
            'ai_result': ai_result,
        })

    def _build_ai_claim_data(self, claim):
        document_names = [
            document.get_document_type_display()
            for document in claim.documents.all()
        ]

        return {
            'claim_id': claim.id,
            'patient_name': claim.patient.full_name,
            'hospital_name': claim.hospital.name,
            'diagnosis': claim.diagnosis,
            'treatment': claim.treatment_type,
            'prescription': self.request.data.get('prescription', ''),
            'lab_test': self.request.data.get('lab_test', ''),
            'bill_amount': float(claim.claimed_amount),
            'policy_limit': float(claim.policy.coverage_amount),
            'deductible': float(claim.policy.deductible_amount),
            'copayment_percent': float(self.request.data.get('copayment_percent', 0)),
            'policy_active': claim.policy.is_active,
            'waiting_period_completed': bool(
                self.request.data.get('waiting_period_completed', True)
            ),
            'hospital_in_network': bool(
                self.request.data.get('hospital_in_network', True)
            ),
            'duplicate_claim': bool(self.request.data.get('duplicate_claim', False)),
            'diagnosis_treatment_mismatch': bool(
                self.request.data.get('diagnosis_treatment_mismatch', False)
            ),
            'previous_claims_count': int(
                self.request.data.get('previous_claims_count', 0)
            ),
            'recent_claims_count': int(
                self.request.data.get('recent_claims_count', 0)
            ),
            'documents': document_names,
        }

    def _save_ai_decision(self, claim, final_decision):
        decision = final_decision.get('decision', Claim.Status.UNDER_REVIEW)
        approved_amount = final_decision.get('approved_amount', 0)
        risk_score = final_decision.get('risk_score')
        explanation = final_decision.get('explanation', '')

        if decision in Claim.Status.values:
            claim.status = decision
        else:
            claim.status = Claim.Status.UNDER_REVIEW

        claim.approved_amount = Decimal(str(approved_amount or 0))
        claim.fraud_score = risk_score
        claim.decision_reason = explanation
        claim.save()
