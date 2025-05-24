from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models.license import License
from ..models.user import User
from ..serializers.license import LicenseSerializer, UserSerializer
from ..serializers.user import UserSerializer as MainUserSerializer
from ..utils import get_user_from_access_token
from drf_spectacular.utils import extend_schema # type: ignore
from ..models.distributor import Distributor
from ..serializers.distributor import DistributorSerializer
from ..permissions import IsAuthenticated

@extend_schema(tags=['Distributor'])
class DistributorViewSet(viewsets.ModelViewSet):
    queryset = Distributor.objects.select_related('created_by', 'verified_by').all()
    serializer_class = DistributorSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='verified')
    def get_verified_distributors(self, request):
        verified_distributors = self.queryset.filter(is_verified=True)
        serializer = self.get_serializer(verified_distributors, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='users')
    def get_user_under_distributor(self, request):
        # Extract master distributor from access token in cookies using utility
        current_distributor = get_user_from_access_token(request, Distributor)
        total_users = User.objects.filter(created_by_distributor=current_distributor).order_by('-date_joined')[:5]
        user_data = MainUserSerializer(total_users, many=True).data
        return Response(user_data)

    @action(detail=False, methods=['get'], url_path='dashboard')
    def dashboard(self, request):
        # Extract master distributor from access token in cookies using utility
        current_distributor = get_user_from_access_token(request, Distributor)

        # Total counts
        total_users = User.objects.filter(created_by_distributor=current_distributor).count()
        total_licenses = License.objects.filter(issued_to_distributor=current_distributor).count()
        active_licenses = License.objects.filter(issued_to_distributor=current_distributor, status='purchased').count()
        available_licenses = License.objects.filter(issued_to_distributor=current_distributor, status='pending').count()

        # Recent records
        recent_users = User.objects.filter(created_by_distributor=current_distributor).order_by('-date_joined')[:5]
        recent_purchased_licenses = License.objects.filter(issued_to_distributor=current_distributor).order_by('-purchased_at')[:5]

        now = timezone.now()
        year = now.year

        # Monthly stats for current year
        purchased_per_month = [0]*12
        sold_per_month = [0]*12
        
        # Get all licenses for the current master distributor for the current year
        licenses = License.objects.filter(issued_to_distributor=current_distributor, created_at__year=year)
        for lic in licenses:
            if lic.created_at:
                if lic.status == 'purchased' and lic.purchased_at:
                    # If the license was purchased from distributor, we count it in the sold_per_month
                    month = lic.purchased_at.month - 1
                    sold_per_month[month] += 1
                else:
                    # If the license was not sold, we count it in the purchased_per_month
                    month = lic.created_at.month - 1
                    purchased_per_month[month] += 1


        # Serializers for recent records
        user_data = UserSerializer(recent_users, many=True).data
        license_data = LicenseSerializer(recent_purchased_licenses, many=True).data

        return Response({
            'total_users': total_users,
            'total_licenses': total_licenses,
            'active_licenses': active_licenses,
            'available_licenses': available_licenses,
            'recent_users': user_data,
            'recent_purchased_licenses': license_data,
            'monthly_stats': {
                'purchased': purchased_per_month,
                'sold': sold_per_month
            }
        })