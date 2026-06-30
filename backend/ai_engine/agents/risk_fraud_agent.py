"""
Risk & Fraud Detection Agent.

This agent calculates a fraud risk score for a health insurance claim.
For now, it uses rule-based scoring. Later, this can be replaced or improved
with a trained ML model such as Random Forest, XGBoost, or Logistic Regression.
"""


class RiskFraudAgent:
    def __init__(self):
        self.high_bill_threshold = 100000
        self.medium_bill_threshold = 50000

    def analyze(self, claim_data, document_result=None, policy_result=None):
        risk_score = 0
        risk_factors = []

        duplicate_result = self._check_duplicate_claim(claim_data)
        bill_result = self._check_bill_risk(claim_data)
        document_risk = self._check_document_risk(document_result)
        medical_risk = self._check_medical_mismatch(claim_data, document_result)
        policy_risk = self._check_policy_risk(policy_result)
        hospital_risk = self._check_hospital_risk(claim_data, policy_result)
        claim_history_risk = self._check_claim_history(claim_data)

        risk_checks = [
            duplicate_result,
            bill_result,
            document_risk,
            medical_risk,
            policy_risk,
            hospital_risk,
            claim_history_risk,
        ]

        for check in risk_checks:
            risk_score += check["score"]
            risk_factors.extend(check["factors"])

        risk_score = min(risk_score, 100)
        risk_level = self._get_risk_level(risk_score)

        return {
            "agent_name": "Risk & Fraud Detection Agent",
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "requires_human_review": risk_score >= 70,
            "risk_summary": self._generate_summary(risk_score, risk_level, risk_factors),
            "checks": {
                "duplicate_claim": duplicate_result,
                "bill_risk": bill_result,
                "document_risk": document_risk,
                "medical_risk": medical_risk,
                "policy_risk": policy_risk,
                "hospital_risk": hospital_risk,
                "claim_history_risk": claim_history_risk,
            },
        }

    def _check_duplicate_claim(self, claim_data):
        score = 0
        factors = []

        if claim_data.get("duplicate_claim", False):
            score += 35
            factors.append("Possible duplicate claim detected.")

        return {
            "score": score,
            "factors": factors,
        }

    def _check_bill_risk(self, claim_data):
        score = 0
        factors = []

        bill_amount = float(claim_data.get("bill_amount", 0))
        policy_limit = float(claim_data.get("policy_limit", 0))

        if bill_amount <= 0:
            score += 20
            factors.append("Invalid or missing bill amount.")

        if bill_amount >= self.high_bill_threshold:
            score += 20
            factors.append("Claim has unusually high bill amount.")
        elif bill_amount >= self.medium_bill_threshold:
            score += 10
            factors.append("Claim has moderately high bill amount.")

        if policy_limit > 0 and bill_amount > policy_limit:
            score += 20
            factors.append("Bill amount exceeds policy coverage limit.")

        return {
            "score": score,
            "factors": factors,
            "bill_amount": bill_amount,
            "policy_limit": policy_limit,
        }

    def _check_document_risk(self, document_result):
        score = 0
        factors = []

        if not document_result:
            return {
                "score": 15,
                "factors": ["Document analysis result is missing."],
            }

        document_status = self._get_nested_value(
            document_result,
            ["document_result", "status"],
            default=document_result.get("status"),
        )

        missing_documents = self._get_nested_value(
            document_result,
            ["document_result", "missing_documents"],
            default=document_result.get("missing_documents", []),
        )

        if document_status == "incomplete":
            score += 25
            factors.append("Required claim documents are incomplete.")

        if missing_documents:
            score += min(len(missing_documents) * 5, 20)
            factors.append(
                "Missing documents: " + ", ".join(missing_documents)
            )

        return {
            "score": score,
            "factors": factors,
            "missing_documents": missing_documents,
        }

    def _check_medical_mismatch(self, claim_data, document_result):
        score = 0
        factors = []

        direct_mismatch = claim_data.get("diagnosis_treatment_mismatch", False)

        agent_match = True
        if document_result:
            agent_match = self._get_nested_value(
                document_result,
                ["medical_result", "diagnosis_treatment_match"],
                default=True,
            )

        if direct_mismatch or agent_match is False:
            score += 30
            factors.append("Diagnosis and treatment information may not match.")

        return {
            "score": score,
            "factors": factors,
        }

    def _check_policy_risk(self, policy_result):
        score = 0
        factors = []

        if not policy_result:
            return {
                "score": 10,
                "factors": ["Policy eligibility result is missing."],
            }

        eligible = policy_result.get("eligible", True)

        if not eligible:
            score += 15
            factors.append("Policy eligibility checks failed.")

        reasons = policy_result.get("reasons", [])
        if reasons:
            factors.extend(reasons[:3])

        return {
            "score": score,
            "factors": factors,
        }

    def _check_hospital_risk(self, claim_data, policy_result):
        score = 0
        factors = []

        hospital_in_network = claim_data.get("hospital_in_network")

        if policy_result:
            hospital_in_network = self._get_nested_value(
                policy_result,
                ["network_result", "hospital_in_network"],
                default=hospital_in_network,
            )

        if hospital_in_network is False:
            score += 10
            factors.append("Hospital is outside approved insurance network.")

        return {
            "score": score,
            "factors": factors,
        }

    def _check_claim_history(self, claim_data):
        score = 0
        factors = []

        previous_claims_count = int(claim_data.get("previous_claims_count", 0))
        recent_claims_count = int(claim_data.get("recent_claims_count", 0))

        if previous_claims_count >= 5:
            score += 10
            factors.append("Patient has high number of previous claims.")

        if recent_claims_count >= 3:
            score += 15
            factors.append("Patient has multiple recent claims in a short period.")

        return {
            "score": score,
            "factors": factors,
            "previous_claims_count": previous_claims_count,
            "recent_claims_count": recent_claims_count,
        }

    def _get_risk_level(self, risk_score):
        if risk_score >= 70:
            return "high"

        if risk_score >= 35:
            return "medium"

        return "low"

    def _generate_summary(self, risk_score, risk_level, risk_factors):
        if not risk_factors:
            return "No major fraud indicators detected."

        return (
            f"Fraud risk is {risk_level} with score {risk_score}. "
            f"Main risk factors: {', '.join(risk_factors[:3])}"
        )

    def _get_nested_value(self, data, keys, default=None):
        current = data

        for key in keys:
            if not isinstance(current, dict) or key not in current:
                return default

            current = current[key]

        return current


if __name__ == "__main__":
    sample_claim = {
        "patient_name": "Ram Sharma",
        "diagnosis": "Appendicitis",
        "treatment": "Appendix Surgery",
        "bill_amount": 120000,
        "policy_limit": 100000,
        "duplicate_claim": False,
        "diagnosis_treatment_mismatch": False,
        "hospital_in_network": True,
        "previous_claims_count": 2,
        "recent_claims_count": 1,
    }

    sample_document_result = {
        "document_result": {
            "status": "complete",
            "missing_documents": [],
        },
        "medical_result": {
            "diagnosis_treatment_match": True,
        },
    }

    sample_policy_result = {
        "eligible": False,
        "network_result": {
            "hospital_in_network": True,
        },
        "reasons": [
            "Claim bill amount exceeds policy coverage limit.",
        ],
    }

    agent = RiskFraudAgent()
    result = agent.analyze(
        claim_data=sample_claim,
        document_result=sample_document_result,
        policy_result=sample_policy_result,
    )

    print(result)