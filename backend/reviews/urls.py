from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HumanReviewViewSet

router = DefaultRouter()
router.register('human-reviews', HumanReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]