from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HospitalViewSet,
    UserProfileViewSet,
    RegisterView,
    VerifyEmailView,
    ResendOTPView,
)

router = DefaultRouter()
router.register('hospitals', HospitalViewSet)
router.register('profiles', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
]