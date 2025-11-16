from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accessibility.utils import user_has_entitlement

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retailer_dashboard(request):
    if not user_has_entitlement(request.user, 'view_retailer_dashboard'):
        return Response({'detail':'Forbidden'}, status=403)
    return Response({'message':'Retailer dashboard data'})
