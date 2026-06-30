"""
Supervisor Agent for Insurance Claim AI Processing.

This agent orchestrates the complete rule-based AI workflow:
1. Document & Medical Analysis Agent
2. Policy & Eligibility Agent
3. Risk & Fraud Detection Agent
4. Claim Decision & Explanation Agent
"""

import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[2]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from ai_engine.agents.document_medical_agent import DocumentMedicalAgent
from ai_engine.agents.policy_eligibility_agent import PolicyEligibilityAgent
from ai_engine.agents.risk_fraud_agent import RiskFraudAgent
from ai_engine.agents.claim_decision_explanation_agent import ClaimDecisionExplanationAgent


class SupervisorAgent:
    def __init__(self):
        self.document_medical_agent = DocumentMedicalAgent()
        self.policy_eligibility_agent = PolicyEligibilityAgent()
        self.risk_fraud_agent = RiskFraudAgent()
        self.claim_decision_explanation_agent = ClaimDecisionExplanationAgent()

    def process_claim(self, claim_data):
        """
        Process one insurance claim through all AI agents.

        Expected claim_data example:
        {
            "patient_name": "Ram Sharma",
            "hospital_name": "City Hospital",
            "diagnosis": "Appendicitis",
            "treatment": "Appendix Surgery",
            "prescription": "Antibiotics and pain medicine",
            "lab_test": "Blood test and ultrasound",
            "bill_amount": 80000,
            "policy_limit": 100000,
            "deductible": 5000,
            "copayment_percent": 10,
            "policy_active": True,
            "waiting_period_completed": True,
            "hospital_in_network": True,
            "duplicate_claim": False,
            "diagnosis_treatment_mismatch": False,
            "documents": [...]
        }
        """

        document_result = self.document_medical_agent.analyze(claim_data)
        policy_result = self.policy_eligibility_agent.analyze(claim_data)
        fraud_result = self.risk_fraud_agent.analyze(
            claim_data=claim_data,
            document_result=document_result,
            policy_result=policy_result,
        )
        final_decision = self.claim_decision_explanation_agent.analyze(
            claim_data=claim_data,
            document_result=document_result,
            policy_result=policy_result,
            fraud_result=fraud_result,
        )

        return {
            "agent_name": "Supervisor Agent",
            "patient_name": claim_data.get("patient_name"),
            "hospital_name": claim_data.get("hospital_name"),
            "diagnosis": claim_data.get("diagnosis"),
            "workflow_status": "completed",
            "document_medical_analysis": document_result,
            "policy_eligibility_analysis": policy_result,
            "risk_fraud_analysis": fraud_result,
            "final_decision": final_decision,
        }


if __name__ == "__main__":
    sample_claim = {
        "patient_name": "Ram Sharma",
        "hospital_name": "City Hospital",
        "diagnosis": "Appendicitis",
        "treatment": "Appendix Surgery",
        "prescription": "Antibiotics and pain medicine",
        "lab_test": "Blood test and ultrasound",
        "bill_amount": 80000,
        "policy_limit": 100000,
        "deductible": 5000,
        "copayment_percent": 10,
        "policy_active": True,
        "waiting_period_completed": True,
        "hospital_in_network": True,
        "duplicate_claim": False,
        "diagnosis_treatment_mismatch": False,
        "previous_claims_count": 2,
        "recent_claims_count": 1,
        "documents": [
            "Insurance Card",
            "Citizenship / ID",
            "Medical Report",
            "Prescription",
            "Hospital Bill",
            "Discharge Summary",
            "Lab Report",
        ],
    }

    supervisor = SupervisorAgent()
    result = supervisor.process_claim(sample_claim)

    print("Supervisor Agent Result:")
    print(result)
