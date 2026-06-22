from rest_framework import viewsets, generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from django.contrib.auth.models import User

from .models import Hospital, UserProfile, EmailOTP
from .serializers import (
    HospitalSerializer,
    UserProfileSerializer,
    RegisterSerializer,
    VerifyOTPSerializer,
    ResendOTPSerializer,
)
from .utils import send_otp_email


class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'register'


class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'verify_email'

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user.is_active = True
        user.save()
        user.email_otp.delete()
        return Response({"message": "Email verified."}, status=status.HTTP_200_OK)


class ResendOTPView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'resend_otp'

    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        otp, _ = EmailOTP.objects.get_or_create(user=user)
        send_otp_email(user, otp.generate())
        return Response({"message": "New code sent."}, status=status.HTTP_200_OK)