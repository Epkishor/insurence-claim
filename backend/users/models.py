from django.db import models
from django.contrib.auth.models import User


class Hospital(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_number = models.CharField(max_length=20)
    registration_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    class Role(models.TextChoices):
        HOSPITAL_STAFF = 'HOSPITAL_STAFF', 'Hospital Staff'
        INSURANCE_OFFICER = 'INSURANCE_OFFICER', 'Insurance Officer'
        REVIEWER = 'REVIEWER', 'Reviewer'
        ADMIN = 'ADMIN', 'Admin'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, choices=Role.choices)
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"