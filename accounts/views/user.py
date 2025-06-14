from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from ..models.user import User, CompanyDetails, Product, Political, Supporters, Party
from ..serializers.user import SupportersSerializer, PoliticalSerializer, ProductSerializer, UserSerializer, UserDetailSerializer, CompanyDetailsSerializer, PartySerializer
from ..permissions import IsAuthenticated
from ..utils import get_user_from_access_token
from ..models.subscription import Subscription
from ..models.license import License
from ..serializers.subscription import SubscriptionSerializer
from ..serializers.license import LicenseSerializer

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
        serializer = UserDetailSerializer(user)
        
        license = License.objects.filter(purchased_by=user).first()
        serializer_data = serializer.data
       
        serializer_data['license_details'] = None
        if license:
            # Serialize all fields from the license instance except 'created_at' and 'updated_at'
            serializer_data['license_details'] = LicenseSerializer(license).data if license else None
        return Response(serializer_data)
    
    @action(detail=True, methods=['post'], url_path='changepassword')
    def change_password(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=404)

        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response({'detail': 'Old and new passwords are required.'}, status=400)

        # Use the check_password method from the User model
        if not user.check_password(old_password):
            return Response({'detail': 'Old password is incorrect.'}, status=400)

        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Password changed successfully.'})
    

@extend_schema(tags=['User -> Company Details'])
class UserCompanyDetailsViewSet(viewsets.ModelViewSet):
    queryset = CompanyDetails.objects.all()
    serializer_class = CompanyDetailsSerializer
    permission_classes = [IsAuthenticated]

@extend_schema(tags=['User -> Products'])
class UserProductDetailsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

@extend_schema(tags=['User -> Political'])
class UserPoliticalViewSet(viewsets.ModelViewSet):
    queryset = Political.objects.all()
    serializer_class = PoliticalSerializer
    permission_classes = [IsAuthenticated]

@extend_schema(tags=['User -> Supporters'])
class UserSupportersViewSet(viewsets.ModelViewSet):
    queryset = Supporters.objects.all()
    serializer_class = SupportersSerializer
    permission_classes = [IsAuthenticated]

@extend_schema(tags=['User -> Party'])
class UserPartyViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
    permission_classes = [IsAuthenticated]