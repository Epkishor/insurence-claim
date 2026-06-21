from rest_framework import viewsets
from .models import ClaimDocument, OCRResult
from .serializers import ClaimDocumentSerializer, OCRResultSerializer
from claims.models import Claim


class ClaimDocumentViewSet(viewsets.ModelViewSet):
    queryset = ClaimDocument.objects.all()
    serializer_class = ClaimDocumentSerializer

    def perform_create(self, serializer):
        document = serializer.save()

        claim = document.claim
        claim.status = Claim.Status.DOCUMENTS_UPLOADED
        claim.save()


class OCRResultViewSet(viewsets.ModelViewSet):
    queryset = OCRResult.objects.all()
    serializer_class = OCRResultSerializer