from rest_framework import viewsets
from .models import HumanReview
from .serializers import HumanReviewSerializer


class HumanReviewViewSet(viewsets.ModelViewSet):
    queryset = HumanReview.objects.all().order_by('-reviewed_at')
    serializer_class = HumanReviewSerializer