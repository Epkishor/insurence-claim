import requests
from django.conf import settings
from django.core.mail import send_mail


def send_otp_email(user, code):
    send_mail(
        subject="Verify your email — Insurance Claim System",
        message=f"Your verification code is {code}. It expires in 10 minutes.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


def verify_turnstile(token, remote_ip=None):
    if not token:
        return False

    payload = {
        "secret": settings.TURNSTILE_SECRET_KEY,
        "response": token,
    }
    if remote_ip:
        payload["remoteip"] = remote_ip

    try:
        resp = requests.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data=payload,
            timeout=5,
        )
        return resp.json().get("success", False)
    except requests.RequestException:
        return False