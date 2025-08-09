from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import AuthenticationFailed
from .models.user import User
from .models.distributor import Distributor
from .models.master_distributor import MasterDistributor

def authenticate_and_get_user(request, model):
    jwt_auth = JWTAuthentication()
    try:
        token = request.COOKIES.get('access_token') or request.headers.get('Authorization', '').split('Bearer ')[-1]
        print('token:', token)
        if not token:
            raise AuthenticationFailed("Token not found in cookies.")

        try:
            validated_token = jwt_auth.get_validated_token(token)
            print('validated_token:', validated_token)
        except Exception:
            raise AuthenticationFailed("Invalid token.")

        user_id = validated_token.payload['user_id']
        print('user_id:', user_id)
        user = model.objects.filter(id=user_id).first()
        print('user:', user)

        if not user:
            print("User not found or invalid token.")
            raise AuthenticationFailed("User not found or invalid token.")

        return user
    except Exception:
        return None

class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        user = authenticate_and_get_user(request, Distributor)
        if user is not None and isinstance(user, Distributor):
            print('authorized as distributor')
            return True

        user = authenticate_and_get_user(request, MasterDistributor)
        if user is not None and isinstance(user, MasterDistributor):
            print('authorized as master distributor')
            return True
        
        user = authenticate_and_get_user(request, User)
        print("user", user)
        if user is not None and isinstance(user, User):
            print('authorized as user')
            return True
        print("isinstance(user, User)", isinstance(user, User))
        print('authorization failed')
        return False
