from rest_framework import viewsets
from .models import ClaimDocument, OCRResult
from .serializers import ClaimDocumentSerializer, OCRResultSerializer


class ClaimDocumentViewSet(viewsets.ModelViewSet):
    queryset = ClaimDocument.objects.all().order_by('-uploaded_at')
    serializer_class = ClaimDocumentSerializer

    def perform_create(self, serializer):
        document = serializer.save()

        claim = document.claim
        claim.status = 'DOCUMENTS_UPLOADED'
        claim.save()


class OCRResultViewSet(viewsets.ModelViewSet):
    queryset = OCRResult.objects.all().order_by('-processed_at')
    serializer_class = OCRResultSerializer