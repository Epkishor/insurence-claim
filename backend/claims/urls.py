from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, ClaimViewSet

router = DefaultRouter()
router.register('patients', PatientViewSet)
router.register('claims', ClaimViewSet)

urlpatterns = [
    path('', include(router.urls)),
]