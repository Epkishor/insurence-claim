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
    ROLE_CHOICES = [
        ('HOSPITAL_STAFF', 'Hospital Staff'),
        ('INSURANCE_OFFICER', 'Insurance Officer'),
        ('REVIEWER', 'Reviewer'),
        ('ADMIN', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"