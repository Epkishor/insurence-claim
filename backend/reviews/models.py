from django.db import models
from django.contrib.auth.models import User
from claims.models import Claim


class HumanReview(models.Model):
    DECISION_CHOICES = [
        ('APPROVE', 'Approve'),
        ('REJECT', 'Reject'),
        ('REQUEST_MORE_DOCUMENTS', 'Request More Documents'),
        ('PARTIALLY_APPROVE', 'Partially Approve'),
    ]

    claim = models.ForeignKey(
        Claim,
        on_delete=models.CASCADE,
        related_name='human_reviews'
    )
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    decision = models.CharField(max_length=40, choices=DECISION_CHOICES)
    approved_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    comment = models.TextField()
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.decision == 'APPROVE':
            self.claim.status = 'APPROVED'
            if self.approved_amount:
                self.claim.approved_amount = self.approved_amount

        elif self.decision == 'PARTIALLY_APPROVE':
            self.claim.status = 'PARTIALLY_APPROVED'
            if self.approved_amount:
                self.claim.approved_amount = self.approved_amount

        elif self.decision == 'REJECT':
            self.claim.status = 'REJECTED'

        elif self.decision == 'REQUEST_MORE_DOCUMENTS':
            self.claim.status = 'MORE_DOCUMENTS_REQUIRED'

        self.claim.decision_reason = self.comment
        self.claim.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review for Claim #{self.claim.id}"