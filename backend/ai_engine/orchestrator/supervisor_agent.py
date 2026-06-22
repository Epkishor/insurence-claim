"""
Supervisor Agent for Insurance Claim AI Processing.

This agent controls the AI workflow. For now, it uses simple internal
rule-based placeholder methods. Later, you can connect it with separate agents:
Document & Medical Analysis Agent, Policy & Eligibility Agent,
Risk & Fraud Detection Agent, and Claim Decision & Explanation Agent.
"""


class SupervisorAgent:
    def __init__(self):
        self.required_documents = {
            "Insurance Card",
            "Citizenship / ID",
            "Medical Report",
            "Prescription",
            "Hospital Bill",
            "Discharge Summary",
            "Lab Report",
        }

    def process_claim(self, claim_data):
        """
        Main method to process one insurance claim.

        Expected claim_data example:
        {
            "patient_name": "Ram Sharma",
            "diagnosis": "Appendicitis",
            "treatment": "Surgery",
            "bill_amount": 80000,
            "policy_limit": 100000,
            "policy_active": True,
            "waiting_period_completed": True,
            "hospital_in_network": True,
            "documents": [
                "Insurance Card",
                "Citizenship / ID",
                "Medical Report",
                "Prescription",
                "Hospital Bill",
                "Discharge Summary",
                "Lab Report"
            ]
        }
        """

        document_result = self._check_documents(claim_data)
        policy_result = self._check_policy_eligibility(claim_data)
        fraud_result = self._check_fraud_risk(claim_data, document_result, policy_result)
        decision_result = self._make_decision(claim_data, document_result, policy_result, fraud_result)

        return {
            "patient_name": claim_data.get("patient_name"),
            "diagnosis": claim_data.get("diagnosis"),
            "document_analysis": document_result,
            "policy_eligibility": policy_result,
            "fraud_analysis": fraud_result,
            "final_decision": decision_result,
        }

    def _check_documents(self, claim_data):
        documents = set(claim_data.get("documents", []))
        missing_documents = sorted(self.required_documents - documents)

        if missing_documents:
            status = "incomplete"
            message = "Some required documents are missing."
        else:
            status = "complete"
            message = "All required documents are submitted."

        return {
            "status": status,
            "submitted_documents": sorted(documents),
            "missing_documents": missing_documents,
            "message": message,
        }

    def _check_policy_eligibility(self, claim_data):
        policy_active = bool(claim_data.get("policy_active", False))
        waiting_period_completed = bool(claim_data.get("waiting_period_completed", False))
        hospital_in_network = bool(claim_data.get("hospital_in_network", False))

        bill_amount = float(claim_data.get("bill_amount", 0))
        policy_limit = float(claim_data.get("policy_limit", 0))

        reasons = []

        if not policy_active:
            reasons.append("Policy is not active.")

        if not waiting_period_completed:
            reasons.append("Waiting period is not completed.")

        if not hospital_in_network:
            reasons.append("Hospital is not in approved network.")

        if bill_amount > policy_limit:
            reasons.append("Bill amount is higher than policy coverage limit.")

        eligible = len(reasons) == 0

        return {
            "eligible": eligible,
            "policy_active": policy_active,
            "waiting_period_completed": waiting_period_completed,
            "hospital_in_network": hospital_in_network,
            "bill_amount": bill_amount,
            "policy_limit": policy_limit,
            "reasons": reasons,
        }

    def _check_fraud_risk(self, claim_data, document_result, policy_result):
        risk_score = 0
        risk_factors = []

        bill_amount = float(claim_data.get("bill_amount", 0))
        policy_limit = float(claim_data.get("policy_limit", 0))

        if document_result["status"] == "incomplete":
            risk_score += 25
            risk_factors.append("Missing required documents.")

        if bill_amount > policy_limit:
            risk_score += 20
            risk_factors.append("Claim amount exceeds policy limit.")

        if claim_data.get("duplicate_claim", False):
            risk_score += 35
            risk_factors.append("Possible duplicate claim detected.")

        if claim_data.get("diagnosis_treatment_mismatch", False):
            risk_score += 30
            risk_factors.append("Diagnosis and treatment information may not match.")

        if not policy_result["hospital_in_network"]:
            risk_score += 10
            risk_factors.append("Hospital is outside approved network.")

        risk_score = min(risk_score, 100)

        if risk_score >= 70:
            risk_level = "high"
        elif risk_score >= 35:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
        }

    def _make_decision(self, claim_data, document_result, policy_result, fraud_result):
        bill_amount = float(claim_data.get("bill_amount", 0))
        policy_limit = float(claim_data.get("policy_limit", 0))

        if document_result["status"] == "incomplete":
            return {
                "decision": "PENDING_DOCUMENTS",
                "approved_amount": 0,
                "requires_human_review": True,
                "explanation": "Claim is pending because required documents are missing.",
            }

        if fraud_result["risk_level"] == "high":
            return {
                "decision": "UNDER_REVIEW",
                "approved_amount": 0,
                "requires_human_review": True,
                "explanation": "Claim requires human review because fraud risk is high.",
            }

        if not policy_result["eligible"]:
            return {
                "decision": "REJECTED",
                "approved_amount": 0,
                "requires_human_review": False,
                "explanation": "Claim rejected because policy eligibility rules are not satisfied.",
                "reasons": policy_result["reasons"],
            }

        approved_amount = min(bill_amount, policy_limit)

        return {
            "decision": "APPROVED",
            "approved_amount": approved_amount,
            "requires_human_review": False,
            "explanation": (
                "Claim approved because all required documents are complete, "
                "policy is eligible, and fraud risk is acceptable."
            ),
        }


if __name__ == "__main__":
    sample_claim = {
        "patient_name": "Ram Sharma",
        "diagnosis": "Appendicitis",
        "treatment": "Appendix Surgery",
        "bill_amount": 80000,
        "policy_limit": 100000,
        "policy_active": True,
        "waiting_period_completed": True,
        "hospital_in_network": True,
        "duplicate_claim": False,
        "diagnosis_treatment_mismatch": False,
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

    print(result)