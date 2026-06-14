from django.db import models


class InsuranceCompany(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class InsurancePolicy(models.Model):
    policy_number = models.CharField(max_length=100, unique=True)
    company = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE)
    policy_holder_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    deductible_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.policy_number


class PolicyClause(models.Model):
    policy = models.ForeignKey(
        InsurancePolicy,
        on_delete=models.CASCADE,
        related_name='clauses'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    clause_type = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.policy.policy_number} - {self.title}"