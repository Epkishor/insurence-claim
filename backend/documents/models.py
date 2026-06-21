from django.db import models
from claims.models import Claim


class ClaimDocument(models.Model):
    class DocumentType(models.TextChoices):
        INSURANCE_CARD = 'INSURANCE_CARD', 'Insurance Card'
        CITIZENSHIP = 'CITIZENSHIP', 'Citizenship / ID'
        MEDICAL_REPORT = 'MEDICAL_REPORT', 'Medical Report'
        PRESCRIPTION = 'PRESCRIPTION', 'Prescription'
        HOSPITAL_BILL = 'HOSPITAL_BILL', 'Hospital Bill'
        DISCHARGE_SUMMARY = 'DISCHARGE_SUMMARY', 'Discharge Summary'
        LAB_REPORT = 'LAB_REPORT', 'Lab Report'
        OTHER = 'OTHER', 'Other'

    claim = models.ForeignKey(
        Claim,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    document_type = models.CharField(max_length=50, choices=DocumentType.choices)
    file = models.FileField(upload_to='claim_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.claim.id} - {self.document_type}"


class OCRResult(models.Model):
    document = models.OneToOneField(
        ClaimDocument,
        on_delete=models.CASCADE,
        related_name='ocr_result'
    )
    extracted_text = models.TextField()
    confidence_score = models.FloatField(null=True, blank=True)
    processed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-processed_at']

    def __str__(self):
        return f"OCR Result for Document #{self.document.id}"