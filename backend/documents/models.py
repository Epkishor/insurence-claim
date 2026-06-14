from django.db import models
from claims.models import Claim


class ClaimDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('INSURANCE_CARD', 'Insurance Card'),
        ('CITIZENSHIP', 'Citizenship / ID'),
        ('MEDICAL_REPORT', 'Medical Report'),
        ('PRESCRIPTION', 'Prescription'),
        ('HOSPITAL_BILL', 'Hospital Bill'),
        ('DISCHARGE_SUMMARY', 'Discharge Summary'),
        ('LAB_REPORT', 'Lab Report'),
        ('OTHER', 'Other'),
    ]

    claim = models.ForeignKey(
        Claim,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    file = models.FileField(upload_to='claim_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

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

    def __str__(self):
        return f"OCR Result for Document #{self.document.id}"