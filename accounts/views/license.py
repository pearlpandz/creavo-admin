from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema # type: ignore
from ..models.license import License
from ..serializers.license import LicenseSerializer

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