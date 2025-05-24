from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from ..models.user import User
from ..serializers.user import UserSerializer
from ..permissions import IsAuthenticated
from ..utils import get_user_from_access_token

@extend_schema(tags=['Application User'])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='active')
    def get_active_users(self, request):
        active_users = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='profile')
    def get_user_from_token(self, request):
        user = get_user_from_access_token(request, User)
        serializer = UserSerializer(user)
        return Response(serializer.data)