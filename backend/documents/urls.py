from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClaimDocumentViewSet, OCRResultViewSet

router = DefaultRouter()
router.register('claim-documents', ClaimDocumentViewSet)
router.register('ocr-results', OCRResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
]