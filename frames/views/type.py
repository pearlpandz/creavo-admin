from rest_framework import viewsets
from accounts.permissions import IsAuthenticated
from frames.serializers.type import FrameTypeSerializer
from frames.models.type import FrameType
from drf_spectacular.utils import extend_schema # type: ignore

@extend_schema(tags=['frametype'])
class FrameTypeViewSet(viewsets.ModelViewSet):
    queryset = FrameType.objects.all()
    serializer_class = FrameTypeSerializer
    # permission_classes = [IsAuthenticated]