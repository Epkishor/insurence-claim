from django.db import models
from django.contrib.auth.models import User
from claims.models import Claim


class HumanReview(models.Model):
    class Decision(models.TextChoices):
        APPROVE = 'APPROVE', 'Approve'
        REJECT = 'REJECT', 'Reject'
        REQUEST_MORE_DOCUMENTS = 'REQUEST_MORE_DOCUMENTS', 'Request More Documents'
        PARTIALLY_APPROVE = 'PARTIALLY_APPROVE', 'Partially Approve'

    claim = models.ForeignKey(
        Claim,
        on_delete=models.CASCADE,
        related_name='human_reviews'
    )
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    decision = models.CharField(max_length=40, choices=Decision.choices)
    approved_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    comment = models.TextField()
    reviewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-reviewed_at']

    # Maps a reviewer decision to the resulting claim status. Keeping this as
    # data (instead of an if/elif chain duplicating Claim.Status) means the
    # mapping is defined once, in one place, and is trivial to extend.
    DECISION_TO_CLAIM_STATUS = {
        Decision.APPROVE: Claim.Status.APPROVED,
        Decision.PARTIALLY_APPROVE: Claim.Status.PARTIALLY_APPROVED,
        Decision.REJECT: Claim.Status.REJECTED,
        Decision.REQUEST_MORE_DOCUMENTS: Claim.Status.MORE_DOCUMENTS_REQUIRED,
    }

    def save(self, *args, **kwargs):
        self.claim.status = self.DECISION_TO_CLAIM_STATUS[self.decision]

        if self.decision in (self.Decision.APPROVE, self.Decision.PARTIALLY_APPROVE) and self.approved_amount:
            self.claim.approved_amount = self.approved_amount

        self.claim.decision_reason = self.comment
        self.claim.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review for Claim #{self.claim.id}"