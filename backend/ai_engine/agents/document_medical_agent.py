"""
Document & Medical Analysis Agent.

This agent checks required claim documents and extracts simple medical details.
For now, it is rule-based. Later, you can connect OCR, NLP, or LLM models here.
"""


class DocumentMedicalAgent:
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

    def analyze(self, claim_data):
        documents_result = self._check_documents(claim_data)
        medical_result = self._analyze_medical_information(claim_data)
        bill_result = self._analyze_bill_information(claim_data)

        return {
            "agent_name": "Document & Medical Analysis Agent",
            "document_result": documents_result,
            "medical_result": medical_result,
            "bill_result": bill_result,
            "overall_status": self._get_overall_status(
                documents_result,
                medical_result,
                bill_result,
            ),
        }

    def _check_documents(self, claim_data):
        submitted_documents = set(claim_data.get("documents", []))
        missing_documents = sorted(self.required_documents - submitted_documents)

        has_discharge_summary = "Discharge Summary" in submitted_documents
        has_medical_report = "Medical Report" in submitted_documents
        has_hospital_bill = "Hospital Bill" in submitted_documents
        has_lab_report = "Lab Report" in submitted_documents

        if missing_documents:
            status = "incomplete"
            message = "Some required documents are missing."
        else:
            status = "complete"
            message = "All required documents are submitted."

        return {
            "status": status,
            "submitted_documents": sorted(submitted_documents),
            "missing_documents": missing_documents,
            "has_discharge_summary": has_discharge_summary,
            "has_medical_report": has_medical_report,
            "has_hospital_bill": has_hospital_bill,
            "has_lab_report": has_lab_report,
            "message": message,
        }

    def _analyze_medical_information(self, claim_data):
        diagnosis = claim_data.get("diagnosis")
        treatment = claim_data.get("treatment")
        prescription = claim_data.get("prescription")
        lab_test = claim_data.get("lab_test")

        issues = []

        if not diagnosis:
            issues.append("Diagnosis information is missing.")

        if not treatment:
            issues.append("Treatment information is missing.")

        if not prescription:
            issues.append("Prescription information is missing.")

        if not lab_test:
            issues.append("Lab test information is missing or not provided.")

        if diagnosis and treatment:
            diagnosis_treatment_match = self._check_diagnosis_treatment_match(
                diagnosis,
                treatment,
            )
        else:
            diagnosis_treatment_match = False

        return {
            "diagnosis": diagnosis,
            "treatment": treatment,
            "prescription": prescription,
            "lab_test": lab_test,
            "diagnosis_treatment_match": diagnosis_treatment_match,
            "issues": issues,
            "status": "valid" if not issues else "needs_review",
        }

    def _analyze_bill_information(self, claim_data):
        bill_amount = float(claim_data.get("bill_amount", 0))
        policy_limit = float(claim_data.get("policy_limit", 0))

        issues = []

        if bill_amount <= 0:
            issues.append("Hospital bill amount is missing or invalid.")

        if policy_limit <= 0:
            issues.append("Policy limit is missing or invalid.")

        if bill_amount > policy_limit and policy_limit > 0:
            issues.append("Bill amount is higher than policy limit.")

        return {
            "bill_amount": bill_amount,
            "policy_limit": policy_limit,
            "is_bill_valid": bill_amount > 0,
            "is_within_policy_limit": bill_amount <= policy_limit if policy_limit > 0 else False,
            "issues": issues,
            "status": "valid" if not issues else "needs_review",
        }

    def _check_diagnosis_treatment_match(self, diagnosis, treatment):
        diagnosis = diagnosis.lower()
        treatment = treatment.lower()

        common_medical_rules = {
            "appendicitis": ["appendix surgery", "appendectomy", "surgery"],
            "fracture": ["cast", "plaster", "surgery", "x-ray"],
            "pneumonia": ["antibiotics", "oxygen", "nebulization"],
            "diabetes": ["insulin", "medicine", "blood sugar monitoring"],
            "heart": ["ecg", "angiography", "cardiac", "medicine"],
            "kidney": ["dialysis", "renal", "medicine"],
        }

        for condition, treatments in common_medical_rules.items():
            if condition in diagnosis:
                return any(item in treatment for item in treatments)

        return True

    def _get_overall_status(self, documents_result, medical_result, bill_result):
        if documents_result["status"] == "incomplete":
            return "incomplete_documents"

        if medical_result["status"] == "needs_review":
            return "medical_review_required"

        if bill_result["status"] == "needs_review":
            return "bill_review_required"

        return "passed"


if __name__ == "__main__":
    sample_claim = {
        "patient_name": "Ram Sharma",
        "diagnosis": "Appendicitis",
        "treatment": "Appendix Surgery",
        "prescription": "Antibiotics and pain medicine",
        "lab_test": "Blood test and ultrasound",
        "bill_amount": 80000,
        "policy_limit": 100000,
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

    agent = DocumentMedicalAgent()
    result = agent.analyze(sample_claim)

    print(result)