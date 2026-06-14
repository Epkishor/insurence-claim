from rest_framework import viewsets, generics
from django.contrib.auth.models import User
from .models import Hospital, UserProfile
from .serializers import HospitalSerializer, UserProfileSerializer, RegisterSerializer


class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer