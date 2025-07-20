from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from django.core.exceptions import ValidationError
from rest_framework import status
from accounts.serializers.user import UserSerializer

def authenticate_user(request, user_model, user_type):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        raise AuthenticationFailed("email and password are required.")

    user = user_model.objects.filter(email=email).first()

    if not user or not check_password(password, user.password):
        raise AuthenticationFailed(f"Invalid credentials for {user_type}.")

    if not user.is_verified:
        raise AuthenticationFailed(f"{user_type} account is not verified.")

    refresh = RefreshToken.for_user(user)

    response = Response({
        "user": {
            "id": user.id,
            "email": user.email,
            "name": f"{user.first_name} {user.last_name}"
        },
    })

    response.set_cookie("refresh_token", str(refresh), httponly=True, secure=True, samesite="None")
    response.set_cookie("access_token", str(refresh.access_token), httponly=True, secure=True, samesite="None")

    return response

def signup_user(request, user_model):
    email = request.data.get("email")
    mobile_number = request.data.get("mobile_number")

    existing_user = user_model.objects.filter(Q(email=email) | Q(mobile_number=mobile_number)).first()

    if existing_user:
        raise ValidationError("A user with this email or mobile number already exists.")

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response = Response({
            "user": {
                "id": user.id,
                "email": user.email,
                "name": f"{user.first_name} {user.last_name}"
            },
        }, status=status.HTTP_201_CREATED)
        response.set_cookie("refresh_token", str(refresh), httponly=True, secure=True, samesite="None")
        response.set_cookie("access_token", str(refresh.access_token), httponly=True, secure=True, samesite="None")
        return response
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def get_user_from_access_token(request, model):
    jwt_auth = JWTAuthentication()
    token = request.COOKIES.get('access_token')
    if not token:
        raise AuthenticationFailed('Token not found in cookies.')
    validated_token = jwt_auth.get_validated_token(token)
    user_id = validated_token.payload['user_id']
    try:
        user = model.objects.get(id=user_id)
    except model.DoesNotExist:
        raise AuthenticationFailed('User not found.')
    return user