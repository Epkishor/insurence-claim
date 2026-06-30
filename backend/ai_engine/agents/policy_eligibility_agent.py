"""
Policy & Eligibility Agent.

This agent checks policy status, coverage limit, hospital network,
waiting period, and exclusions. Later, the policy clause method can be
replaced with RAG/vector database retrieval.
"""


class PolicyEligibilityAgent:
    def __init__(self):
        self.default_excluded_treatments = {
            "cosmetic surgery",
            "experimental treatment",
            "non medical treatment",
            "self inflicted injury",
            "fertility treatment",
        }

    def analyze(self, claim_data):
        policy_status = self._check_policy_status(claim_data)
        coverage_result = self._check_coverage_limit(claim_data)
        network_result = self._check_hospital_network(claim_data)
        waiting_period_result = self._check_waiting_period(claim_data)
        exclusion_result = self._check_exclusions(claim_data)

        eligible = all(
            [
                policy_status["is_active"],
                coverage_result["within_coverage"],
                network_result["hospital_in_network"],
                waiting_period_result["waiting_period_completed"],
                not exclusion_result["has_exclusion"],
            ]
        )

        reasons = []
        reasons.extend(policy_status["reasons"])
        reasons.extend(coverage_result["reasons"])
        reasons.extend(network_result["reasons"])
        reasons.extend(waiting_period_result["reasons"])
        reasons.extend(exclusion_result["reasons"])

        return {
            "agent_name": "Policy & Eligibility Agent",
            "eligible": eligible,
            "policy_status": policy_status,
            "coverage_result": coverage_result,
            "network_result": network_result,
            "waiting_period_result": waiting_period_result,
            "exclusion_result": exclusion_result,
            "policy_clauses_used": self._get_policy_clauses(reasons),
            "reasons": reasons,
            "overall_status": "eligible" if eligible else "not_eligible",
        }

    def _check_policy_status(self, claim_data):
        policy_active = bool(claim_data.get("policy_active", False))
        reasons = []

        if not policy_active:
            reasons.append("Insurance policy is not active.")

        return {
            "is_active": policy_active,
            "reasons": reasons,
        }

    def _check_coverage_limit(self, claim_data):
        bill_amount = float(claim_data.get("bill_amount", 0))
        policy_limit = float(claim_data.get("policy_limit", 0))
        reasons = []

        if policy_limit <= 0:
            reasons.append("Policy coverage limit is missing or invalid.")

        if bill_amount <= 0:
            reasons.append("Claim bill amount is missing or invalid.")

        if policy_limit > 0 and bill_amount > policy_limit:
            reasons.append("Claim bill amount exceeds policy coverage limit.")

        return {
            "bill_amount": bill_amount,
            "policy_limit": policy_limit,
            "within_coverage": bill_amount > 0 and policy_limit > 0 and bill_amount <= policy_limit,
            "reasons": reasons,
        }

    def _check_hospital_network(self, claim_data):
        hospital_in_network = bool(claim_data.get("hospital_in_network", False))
        reasons = []

        if not hospital_in_network:
            reasons.append("Hospital is not inside the approved insurance network.")

        return {
            "hospital_name": claim_data.get("hospital_name", "Unknown Hospital"),
            "hospital_in_network": hospital_in_network,
            "reasons": reasons,
        }

    def _check_waiting_period(self, claim_data):
        waiting_period_completed = bool(claim_data.get("waiting_period_completed", False))
        reasons = []

        if not waiting_period_completed:
            reasons.append("Policy waiting period has not been completed.")

        return {
            "waiting_period_completed": waiting_period_completed,
            "reasons": reasons,
        }

    def _check_exclusions(self, claim_data):
        diagnosis = str(claim_data.get("diagnosis", "")).lower()
        treatment = str(claim_data.get("treatment", "")).lower()
        excluded_treatments = set(
            claim_data.get("excluded_treatments", self.default_excluded_treatments)
        )
        matched_exclusions = []

        for excluded_item in excluded_treatments:
            excluded_item_lower = excluded_item.lower()
            if excluded_item_lower in diagnosis or excluded_item_lower in treatment:
                matched_exclusions.append(excluded_item)

        reasons = []
        if matched_exclusions:
            reasons.append(
                "Claim contains excluded treatment or condition: "
                + ", ".join(matched_exclusions)
            )

        return {
            "has_exclusion": len(matched_exclusions) > 0,
            "matched_exclusions": matched_exclusions,
            "reasons": reasons,
        }

    def _get_policy_clauses(self, reasons):
        clauses = [
            {
                "clause_id": "POLICY-ACTIVE-001",
                "title": "Active Policy Requirement",
                "text": "The insurance policy must be active on the date of treatment.",
            },
            {
                "clause_id": "COVERAGE-LIMIT-001",
                "title": "Coverage Limit Rule",
                "text": "The payable claim amount cannot exceed the available policy coverage limit.",
            },
            {
                "clause_id": "NETWORK-HOSPITAL-001",
                "title": "Hospital Network Rule",
                "text": "Treatment should be taken from an approved hospital network unless emergency rules apply.",
            },
            {
                "clause_id": "WAITING-PERIOD-001",
                "title": "Waiting Period Rule",
                "text": "Claims are eligible only after the required waiting period is completed.",
            },
        ]

        if reasons:
            clauses.append(
                {
                    "clause_id": "EXCLUSION-001",
                    "title": "Exclusion Rule",
                    "text": "Claims matching policy exclusions may be rejected or sent for review.",
                }
            )

        return clauses
