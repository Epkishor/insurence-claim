from django.contrib import admin
from .models import ClaimDocument, OCRResult

admin.site.register(ClaimDocument)
admin.site.register(OCRResult)