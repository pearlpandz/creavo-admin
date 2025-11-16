from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

signer = TimestampSigner()

def make_email_token(email: str) -> str:
    return signer.sign(email)

def verify_email_token(token: str, max_age=60*60*24) -> str:
    try:
        email = signer.unsign(token, max_age=max_age)
        return email
    except SignatureExpired:
        raise
    except BadSignature:
        raise

def send_verification_email(user, request):
    token = make_email_token(user.email)
    verify_url = request.build_absolute_uri(reverse('verify-email') + f'?token={token}')
    subject = 'Verify your account'
    message = f'Click to verify: {verify_url}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
