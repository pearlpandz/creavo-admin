from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from ..models.user import User
from ..models.distributor import Distributor
from ..models.master_distributor import MasterDistributor
from ..utils import authenticate_user, signup_user
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

@extend_schema(request={
    'application/json': {
        'type': 'object',
        'properties': {
            'email': {'type': 'string'},
            'password': {'type': 'string'}
        },
        'required': ['email', 'password']
    }
})
class UserAuthenticationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return authenticate_user(request, User, "User")
    
@extend_schema(request={
    'application/json': {
        'type': 'object',
        'properties': {
            'first_name': {'type': 'string'},
            'last_name': {'type': 'string'},
            'email': {'type': 'string'},
            'mobile_number': {'type': 'string'},
            'password': {'type': 'string'}
        },
        'required': ['email', 'password']
    }
})
class UserRegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return signup_user(request, User)

@extend_schema(request={
    'application/json': {
        'type': 'object',
        'properties': {
            'email': {'type': 'string'},
            'password': {'type': 'string'}
        },
        'required': ['email', 'password']
    }
})
class DistributorAuthenticationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return authenticate_user(request, Distributor, "Distributor")

@extend_schema(request={
    'application/json': {
        'type': 'object',
        'properties': {
            'email': {'type': 'string'},
            'password': {'type': 'string'}
        },
        'required': ['email', 'password']
    }
})
class MasterDistributorAuthenticationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return authenticate_user(request, MasterDistributor, "Master Distributor")


@ensure_csrf_cookie
def get_csrf(request):
    return JsonResponse({'detail': 'CSRF cookie set'})