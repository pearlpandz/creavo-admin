from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from .models import Entitlement, RoleEntitlement
from .serializers import EntitlementSerializer, RoleEntitlementSerializer

class EntitlementViewSet(viewsets.ModelViewSet):
    queryset = Entitlement.objects.all()
    serializer_class = EntitlementSerializer
    permission_classes = [IsAdminUser]

class RoleEntitlementViewSet(viewsets.ModelViewSet):
    queryset = RoleEntitlement.objects.select_related('entitlement').all()
    serializer_class = RoleEntitlementSerializer
    permission_classes = [IsAdminUser]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_entitlements(request):
    role = request.user.role
    items = RoleEntitlement.objects.filter(role=role).select_related('entitlement')
    serializer = RoleEntitlementSerializer(items, many=True)
    return Response({'role': role, 'entitlements': serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def has_access(request, entitlement_name):
    exists = RoleEntitlement.objects.filter(role=request.user.role, entitlement__name=entitlement_name).exists()
    return Response({'entitlement': entitlement_name, 'access': exists})
