from django.contrib import admin
from .models import InsuranceCompany, InsurancePolicy, PolicyClause

admin.site.register(InsuranceCompany)
admin.site.register(InsurancePolicy)
admin.site.register(PolicyClause)