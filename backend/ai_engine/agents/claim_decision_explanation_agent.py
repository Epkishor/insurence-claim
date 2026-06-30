"""
Claim Decision & Explanation Agent.

This agent generates the final claim decision using outputs from:
1. Document & Medical Analysis Agent
2. Policy & Eligibility Agent
3. Risk & Fraud Detection Agent

For now, it is rule-based. Later, it can be improved with LLM-based
explanations, SHAP/LIME, and RAG-based policy citation.
"""


class ClaimDecisionExplanationAgent:
    def __init__(self):
        self.high_risk_threshold = 70
        self.medium_risk_threshold = 35

    def analyze(self, claim_data, document_result=None, policy_result=None, fraud_result=None):
        document_status = self._get_document_status(document_result)
        policy_eligible = self._get_policy_eligibility(policy_result)
        risk_score = self._get_risk_score(fraud_result)
        risk_level = self._get_risk_level(fraud_result, risk_score)

        decision = self._decide_claim(
            document_status=document_status,
            policy_eligible=policy_eligible,
            risk_score=risk_score,
            risk_level=risk_level,
        )

        approved_amount = self._calculate_approved_amount(
            claim_data=claim_data,
            decision=decision,
            policy_result=policy_result,
        )

        explanation = self._generate_explanation(
            decision=decision,
            approved_amount=approved_amount,
            document_result=document_result,
            policy_result=policy_result,
            fraud_result=fraud_result,
        )

        return {
            "agent_name": "Claim Decision & Explanation Agent",
            "decision": decision,
            "approved_amount": approved_amount,
            "requires_human_review": decision in ["UNDER_REVIEW", "PENDING_DOCUMENTS"],
            "risk_score": risk_score,
            "risk_level": risk_level,
            "policy_clauses_used": self._get_policy_clauses(policy_result),
            "explanation": explanation,
            "summary": self._generate_summary(decision, approved_amount, risk_score),
        }

    def _decide_claim(self, document_status, policy_eligible, risk_score, risk_level):
        if document_status == "incomplete":
            return "PENDING_DOCUMENTS"

        if risk_score >= self.high_risk_threshold or risk_level == "high":
            return "UNDER_REVIEW"

        if not policy_eligible:
            return "REJECTED"

        return "APPROVED"

    def _calculate_approved_amount(self, claim_data, decision, policy_result):
        if decision != "APPROVED":
            return 0.0

        bill_amount = float(claim_data.get("bill_amount", 0))
        policy_limit = float(claim_data.get("policy_limit", 0))
        deductible = float(claim_data.get("deductible", 0))
        copayment_percent = float(claim_data.get("copayment_percent", 0))

        if policy_result:
            coverage_result = policy_result.get("coverage_result", {})
            bill_amount = float(coverage_result.get("bill_amount", bill_amount))
            policy_limit = float(coverage_result.get("policy_limit", policy_limit))

        base_amount = min(bill_amount, policy_limit)

        after_deductible = max(base_amount - deductible, 0)

        copayment_amount = after_deductible * (copayment_percent / 100)

        approved_amount = after_deductible - copayment_amount

        return round(approved_amount, 2)

    def _generate_explanation(self, decision, approved_amount, document_result, policy_result, fraud_result):
        explanation_parts = []

        if decision == "APPROVED":
            explanation_parts.append(
                "Claim approved because required documents are complete, "
                "policy eligibility rules are satisfied, and fraud risk is acceptable."
            )
            explanation_parts.append(f"Final payable amount is {approved_amount}.")

        elif decision == "PENDING_DOCUMENTS":
            missing_documents = self._get_missing_documents(document_result)
            explanation_parts.append(
                "Claim is pending because required documents are missing or incomplete."
            )

            if missing_documents:
                explanation_parts.append(
                    "Missing documents: " + ", ".join(missing_documents) + "."
                )

        elif decision == "UNDER_REVIEW":
            risk_score = self._get_risk_score(fraud_result)
            risk_factors = self._get_risk_factors(fraud_result)

            explanation_parts.append(
                f"Claim is sent for human review because fraud risk score is {risk_score}."
            )

            if risk_factors:
                explanation_parts.append(
                    "Main risk factors: " + ", ".join(risk_factors[:3]) + "."
                )

        elif decision == "REJECTED":
            policy_reasons = self._get_policy_reasons(policy_result)

            explanation_parts.append(
                "Claim rejected because policy eligibility rules are not satisfied."
            )

            if policy_reasons:
                explanation_parts.append(
                    "Reasons: " + ", ".join(policy_reasons) + "."
                )

        return " ".join(explanation_parts)

    def _generate_summary(self, decision, approved_amount, risk_score):
        return {
            "claim_status": decision,
            "approved_amount": approved_amount,
            "fraud_risk_score": risk_score,
            "message": self._summary_message(decision),
        }

    def _summary_message(self, decision):
        messages = {
            "APPROVED": "Claim is approved for payment.",
            "REJECTED": "Claim is rejected based on policy rules.",
            "PENDING_DOCUMENTS": "Claim is pending due to missing documents.",
            "UNDER_REVIEW": "Claim requires human review due to high risk.",
        }

        return messages.get(decision, "Claim decision generated.")

    def _get_document_status(self, document_result):
        if not document_result:
            return "incomplete"

        if "document_result" in document_result:
            return document_result["document_result"].get("status", "incomplete")

        return document_result.get("status", "incomplete")

    def _get_policy_eligibility(self, policy_result):
        if not policy_result:
            return False

        return bool(policy_result.get("eligible", False))

    def _get_risk_score(self, fraud_result):
        if not fraud_result:
            return 100

        return int(fraud_result.get("risk_score", 100))

    def _get_risk_level(self, fraud_result, risk_score):
        if fraud_result:
            return fraud_result.get("risk_level", self._risk_level_from_score(risk_score))

        return self._risk_level_from_score(risk_score)

    def _risk_level_from_score(self, risk_score):
        if risk_score >= self.high_risk_threshold:
            return "high"

        if risk_score >= self.medium_risk_threshold:
            return "medium"

        return "low"

    def _get_missing_documents(self, document_result):
        if not document_result:
            return []

        if "document_result" in document_result:
            return document_result["document_result"].get("missing_documents", [])

        return document_result.get("missing_documents", [])

    def _get_policy_reasons(self, policy_result):
        if not policy_result:
            return ["Policy eligibility result is missing."]

        return policy_result.get("reasons", [])

    def _get_risk_factors(self, fraud_result):
        if not fraud_result:
            return ["Fraud analysis result is missing."]

        return fraud_result.get("risk_factors", [])

    def _get_policy_clauses(self, policy_result):
        if not policy_result:
            return []

        return policy_result.get("policy_clauses_used", [])


if __name__ == "__main__":
    sample_claim = {
        "patient_name": "Ram Sharma",
        "diagnosis": "Appendicitis",
        "treatment": "Appendix Surgery",
        "bill_amount": 80000,
        "policy_limit": 100000,
        "deductible": 5000,
        "copayment_percent": 10,
    }

    sample_document_result = {
        "document_result": {
            "status": "complete",
            "missing_documents": [],
        }
    }

    sample_policy_result = {
        "eligible": True,
        "coverage_result": {
            "bill_amount": 80000,
            "policy_limit": 100000,
        },
        "reasons": [],
        "policy_clauses_used": [
            {
                "clause_id": "COVERAGE-LIMIT-001",
                "title": "Coverage Limit Rule",
                "text": "The payable claim amount cannot exceed the policy coverage limit.",
            }
        ],
    }

    sample_fraud_result = {
        "risk_score": 20,
        "risk_level": "low",
        "risk_factors": [],
    }

    agent = ClaimDecisionExplanationAgent()
    result = agent.analyze(
        claim_data=sample_claim,
        document_result=sample_document_result,
        policy_result=sample_policy_result,
        fraud_result=sample_fraud_result,
    )

    print(result)