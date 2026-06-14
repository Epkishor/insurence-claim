from django.contrib import admin
from .models import Patient, Claim

admin.site.register(Patient)
admin.site.register(Claim)