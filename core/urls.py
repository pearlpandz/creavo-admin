from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    register, verify_email, me, profile_patch,
    password_reset_request, password_reset_confirm, change_password,
    send_mobile_otp, verify_mobile_otp, create_child_user
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', register, name='register'),
    path('verify-email/', verify_email, name='verify-email'),

    path('me/', me, name='me'),
    path('me/patch/', profile_patch, name='profile_patch'),

    path('password-reset/', password_reset_request, name='password_reset'),
    path('password-reset-confirm/', password_reset_confirm, name='password_reset_confirm'),
    path('change-password/', change_password, name='change_password'),

    path('phone/send-otp/', send_mobile_otp, name='send_mobile_otp'),
    path('phone/verify-otp/', verify_mobile_otp, name='verify_mobile_otp'),

    path('create-child/', create_child_user, name='create_child_user'),
]
