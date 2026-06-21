from django.db import models
from users.models import Hospital
from policies.models import InsurancePolicy


class Patient(models.Model):
    full_name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    insurance_number = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


class Claim(models.Model):
    class Status(models.TextChoices):
        PENDING_DOCUMENTS = 'PENDING_DOCUMENTS', 'Pending Documents'
        DOCUMENTS_UPLOADED = 'DOCUMENTS_UPLOADED', 'Documents Uploaded'
        PROCESSING = 'PROCESSING', 'Processing'
        UNDER_REVIEW = 'UNDER_REVIEW', 'Under Review'
        APPROVED = 'APPROVED', 'Approved'
        PARTIALLY_APPROVED = 'PARTIALLY_APPROVED', 'Partially Approved'
        REJECTED = 'REJECTED', 'Rejected'
        MORE_DOCUMENTS_REQUIRED = 'MORE_DOCUMENTS_REQUIRED', 'More Documents Required'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    policy = models.ForeignKey(InsurancePolicy, on_delete=models.CASCADE)

    diagnosis = models.CharField(max_length=255)
    treatment_type = models.CharField(max_length=255)
    admission_date = models.DateField()
    discharge_date = models.DateField(null=True, blank=True)

    claimed_amount = models.DecimalField(max_digits=12, decimal_places=2)
    approved_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=40,
        choices=Status.choices,
        default=Status.PENDING_DOCUMENTS
    )

    fraud_score = models.FloatField(null=True, blank=True)
    decision_reason = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def calculate_approved_amount(self):
        policy_limit = self.policy.coverage_amount
        deductible = self.policy.deductible_amount

        approved = min(self.claimed_amount, policy_limit) - deductible

        if approved < 0:
            approved = 0

        self.approved_amount = approved
        return approved

    def __str__(self):
        return f"Claim #{self.id} - {self.patient.full_name}"