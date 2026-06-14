from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InsuranceCompanyViewSet, InsurancePolicyViewSet, PolicyClauseViewSet

router = DefaultRouter()
router.register('companies', InsuranceCompanyViewSet)
router.register('policies', InsurancePolicyViewSet)
router.register('clauses', PolicyClauseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]