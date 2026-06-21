from rest_framework import viewsets
from .models import HumanReview
from .serializers import HumanReviewSerializer


class HumanReviewViewSet(viewsets.ModelViewSet):
    queryset = HumanReview.objects.all()
    serializer_class = HumanReviewSerializer