from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from ..permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema # type: ignore
from ..models.license import License
from ..serializers.license import LicenseSerializer
from django.utils import timezone
from ..models.user import User
@extend_schema(tags=['License'])
class LicenseViewSet(viewsets.ModelViewSet):
    queryset = License.objects.all()
    serializer_class = LicenseSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='status/(?P<status>[^/.]+)')
    def get_licenses_by_status(self, request, status=None):
        if status in ['available', 'purchased']:
            filtered_licenses = self.queryset.filter(status=status)
            serializer = self.get_serializer(filtered_licenses, many=True)
            return Response(serializer.data)
        return Response([])

    @action(detail=False, methods=['get'], url_path='code/(?P<code>[^/.]+)')
    def get_license_by_code(self, request, code=None):
        from uuid import UUID
        try:
            code_uuid = UUID(code)  # Convert the code to a UUID
            license_obj = self.queryset.get(code=code_uuid)
            serializer = self.get_serializer(license_obj)
            return Response(serializer.data)
        except ValueError:
            return Response({'error': 'Invalid UUID format for code.'}, status=400)
        except License.DoesNotExist:
            return Response({'error': 'License not found'}, status=404)
        
    @action(detail=False, methods=['post'], url_path='purchase')
    def purchase_license(self, request):
        """
        Assigns a license to a user by updating purchased_by, purchased_at, and status.
        Expects payload: { userId, licenseId }
        Returns: license code and purchased_date
        """
        user_id = request.data.get('user_id')
        code = request.data.get('license_code')
        if not user_id or not code:
            return Response({'error': 'userId and licenseId are required.'}, status=400)
        
        # Update license model
        try:
            license_obj = License.objects.get(code=code)
        except License.DoesNotExist:
            return Response({'error': 'License not found.'}, status=404)
        purchased_at = timezone.now()
        license_obj.purchased_by_id = user_id
        license_obj.purchased_at = purchased_at
        license_obj.status = 'purchased'
        license_obj.save()

        # Update user model
        try:
            user_obj = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)
        user_obj.license = str(license_obj.code)
        user_obj.purchased_date = purchased_at.date()
        user_obj.save()
        
        serializer = LicenseSerializer(license_obj)
        return Response({
            'message': 'purchased successfully',
            'license_details': serializer.data,
            'userid': user_id
        })

@api_view(['GET'])
def licenses_by_distributor(request, distributor_id):
    licenses = License.objects.filter(issued_to_distributor_id=distributor_id)
    serializer = LicenseSerializer(licenses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def licenses_by_master_distributor(request, master_distributor_id):
    licenses = License.objects.filter(issued_to_master_distributor_id=master_distributor_id)
    serializer = LicenseSerializer(licenses, many=True)
    return Response(serializer.data)