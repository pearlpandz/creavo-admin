from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from .serializers import UserSerializer, RegisterSerializer, ProfileSerializer, ProfilePatchSerializer
from .utils import send_verification_email, verify_email_token
from .models import PhoneOTP
from .hierarchy import ALLOWED_CHILD
import random

User = get_user_model()
token_generator = PasswordResetTokenGenerator()

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    send_verification_email(user, request)
    return Response({'detail':'User created. Check email to verify.'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request):
    token = request.query_params.get('token')
    if not token:
        return Response({'detail':'token required'}, status=400)
    try:
        email = verify_email_token(token)
    except Exception:
        return Response({'detail':'invalid or expired token'}, status=400)
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'detail':'user not found'}, status=404)
    user.is_active = True
    user.save()
    return Response({'detail':'email verified. You can login now.'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    serializer = ProfileSerializer(request.user)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def profile_patch(request):
    serializer = ProfilePatchSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    email = request.data.get('email')
    if not email:
        return Response({'detail':'email required'}, status=400)
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'detail':'ok'}, status=200)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)
    reset_url = request.build_absolute_uri(f"/api/auth/password-reset-confirm/?uid={uid}&token={token}")
    from django.core.mail import send_mail
    send_mail('Password reset', f'Reset here: {reset_url}', settings.DEFAULT_FROM_EMAIL, [email])
    return Response({'detail':'ok'})

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    uidb64 = request.data.get('uid')
    token = request.data.get('token')
    new_password = request.data.get('password')
    if not all([uidb64, token, new_password]):
        return Response({'detail':'uid, token, password required'}, status=400)
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        return Response({'detail':'invalid'}, status=400)
    if not token_generator.check_token(user, token):
        return Response({'detail':'invalid token'}, status=400)
    user.set_password(new_password)
    user.save()
    return Response({'detail':'password set'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old = request.data.get('old_password')
    new = request.data.get('new_password')
    if not user.check_password(old):
        return Response({'detail':'old password incorrect'}, status=400)
    user.set_password(new)
    user.save()
    return Response({'detail':'password changed'})

@api_view(['POST'])
@permission_classes([AllowAny])
def send_mobile_otp(request):
    phone = request.data.get('phone')
    if not phone:
        return Response({'detail':'phone required'}, status=400)
    otp = f"{random.randint(100000,999999)}"
    PhoneOTP.objects.create(phone=phone, otp=otp)
    print('OTP for', phone, otp)
    return Response({'detail':'otp_sent'})

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_mobile_otp(request):
    phone = request.data.get('phone'); otp = request.data.get('otp')
    if not all([phone, otp]):
        return Response({'detail':'phone and otp required'}, status=400)
    po = PhoneOTP.objects.filter(phone=phone).order_by('-created_at').first()
    if not po or not po.is_valid():
        return Response({'detail':'otp invalid or expired'}, status=400)
    if po.otp != otp:
        return Response({'detail':'otp mismatch'}, status=400)
    user = request.user if request.user and request.user.is_authenticated else None
    if user:
        user.phone_verified = True
        user.phone_number = phone
        user.save()
    return Response({'detail':'phone verified'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_child_user(request):
    current_role = request.user.role
    allowed = ALLOWED_CHILD.get(current_role, [])
    desired_role = request.data.get('role')
    if desired_role not in allowed:
        return Response({'detail':'cannot create this role'}, status=403)
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    user.is_active = True
    user.parent = request.user
    user.created_by = request.user
    user.save()
    return Response({'detail':'user created','user_id':user.id}, status=201)
