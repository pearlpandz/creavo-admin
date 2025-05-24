from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema # type: ignore
from django.utils import timezone
from ..models.master_distributor import MasterDistributor
from ..serializers.master_distributor import MasterDistributorSerializer
from ..permissions import IsAuthenticated
from ..models.distributor import Distributor
from ..models.user import User
from ..models.license import License
from ..utils import get_user_from_access_token
from ..serializers.license import LicenseSerializer, UserSerializer, DistributorSerializer
from ..serializers.user import UserSerializer as MainUserSerializer
from ..serializers.distributor import DistributorSerializer as MainDistributorSerializer

@extend_schema(tags=['Master Distributor'])
class MasterDistributorViewSet(viewsets.ModelViewSet):
    queryset = MasterDistributor.objects.all()
    serializer_class = MasterDistributorSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='verified')
    def get_verified_distributors(self, request):
        verified_distributors = self.queryset.filter(is_verified=True)
        serializer = self.get_serializer(verified_distributors, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='users')
    def get_user_under_master_distributor(self, request):
        # Extract master distributor from access token in cookies using utility
        current_distributor = get_user_from_access_token(request, MasterDistributor)
        total_users = User.objects.filter(created_by_master_distributor=current_distributor).order_by('-date_joined')[:5]
        user_data = MainUserSerializer(total_users, many=True).data
        return Response(user_data)
    
    @action(detail=False, methods=['get'], url_path='distributors')
    def get_distributor_under_master(self, request):
        # Extract master distributor from access token in cookies using utility
        current_distributor = get_user_from_access_token(request, MasterDistributor)
        total_users = Distributor.objects.filter(created_by=current_distributor).order_by('-created_at')[:5]
        user_data = MainDistributorSerializer(total_users, many=True).data
        return Response(user_data)

    @action(detail=False, methods=['get'], url_path='dashboard')
    def dashboard(self, request):
        print("Dashboard view called")
        # Extract master distributor from access token in cookies using utility
        current_master_distributor = get_user_from_access_token(request, MasterDistributor)

        # Total counts
        total_distributors = Distributor.objects.filter(created_by=current_master_distributor).count()
        total_users = User.objects.filter(created_by_master_distributor=current_master_distributor).count()
        total_licenses = License.objects.filter(issued_to_master_distributor=current_master_distributor).count()
        active_licenses = License.objects.filter(issued_to_master_distributor=current_master_distributor, status='purchased').count()

        # Recent records
        recent_distributors = Distributor.objects.filter(created_by=current_master_distributor).order_by('-created_at')[:5]
        recent_users = User.objects.filter(created_by_master_distributor=current_master_distributor).order_by('-date_joined')[:5]
        recent_purchased_licenses = License.objects.filter(issued_to_master_distributor=current_master_distributor).order_by('-purchased_at')[:5]

        now = timezone.now()
        year = now.year

        # Monthly stats for current year
        purchased_per_month = [0]*12
        sold_per_month = [0]*12

        # Get all licenses for the current master distributor for the current year
        licenses = License.objects.filter(issued_to_master_distributor=current_master_distributor, created_at__year=year)
        for lic in licenses:
            if lic.created_at:
                if lic.status == 'purchased' and lic.purchased_at:
                    # If the license was purchased, we count it in the sold_per_month
                    month = lic.purchased_at.month - 1
                    sold_per_month[month] += 1
                else:
                    # If the license was sold, we count it in the unsold_per_month
                    month = lic.created_at.month - 1
                    purchased_per_month[month] += 1


        # Serializers for recent records
        distributor_data = DistributorSerializer(recent_distributors, many=True).data
        user_data = UserSerializer(recent_users, many=True).data
        license_data = LicenseSerializer(recent_purchased_licenses, many=True).data

        return Response({
            'total_distributors': total_distributors,
            'total_users': total_users,
            'total_licenses': total_licenses,
            'active_licenses': active_licenses,
            'recent_distributors': distributor_data,
            'recent_users': user_data,
            'recent_purchased_licenses': license_data,
            'monthly_stats': {
                'purchased': purchased_per_month,
                'sold': sold_per_month
            }
        })
    