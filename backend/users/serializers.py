from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Hospital, UserProfile, EmailOTP
from .utils import send_otp_email, verify_turnstile


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'role', 'hospital']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(write_only=True)
    turnstile_token = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'turnstile_token']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def validate_turnstile_token(self, value):
        request = self.context.get('request')
        remote_ip = request.META.get('REMOTE_ADDR') if request else None
        if not verify_turnstile(value, remote_ip):
            raise serializers.ValidationError("Verification check failed. Please try again.")
        return value

    def create(self, validated_data):
        validated_data.pop('turnstile_token', None)
        role = validated_data.pop('role')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            is_active=False,
        )

        UserProfile.objects.create(user=user, role=role)

        otp = EmailOTP.objects.create(user=user)
        send_otp_email(user, otp.generate())

        return user


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("No account with this email.")

        if user.is_active:
            raise serializers.ValidationError("Email already verified.")

        try:
            otp = user.email_otp
        except EmailOTP.DoesNotExist:
            raise serializers.ValidationError("No OTP found. Request a new code.")

        if otp.is_expired():
            raise serializers.ValidationError("Code expired. Request a new one.")
        if otp.attempts >= 5:
            raise serializers.ValidationError("Too many attempts. Request a new code.")
        if otp.code != data["code"]:
            otp.attempts += 1
            otp.save()
            raise serializers.ValidationError("Incorrect code.")

        data["user"] = user
        return data


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    turnstile_token = serializers.CharField(write_only=True)

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No account with this email.")
        if user.is_active:
            raise serializers.ValidationError("Email already verified.")
        self.user = user
        return value

    def validate_turnstile_token(self, value):
        request = self.context.get('request')
        remote_ip = request.META.get('REMOTE_ADDR') if request else None
        if not verify_turnstile(value, remote_ip):
            raise serializers.ValidationError("Verification check failed. Please try again.")
        return value