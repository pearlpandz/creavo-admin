from rest_framework import viewsets
from accounts.permissions import IsAuthenticated
from frames.serializers.type import FrameTypeSerializer
from frames.models.type import FrameType
from drf_spectacular.utils import extend_schema # type: ignore
from rest_framework.decorators import action
import requests
from rest_framework.response import Response

@extend_schema(tags=['frametype'])
class FrameTypeViewSet(viewsets.ModelViewSet):
    queryset = FrameType.objects.all()
    serializer_class = FrameTypeSerializer
    # permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='list')
    def category_list(self, request):
        frametypes = self.get_queryset()
        serializer = self.get_serializer(frametypes, many=True)

        # Fetch counts from external API
        try:
            resp = requests.get("https://frame-service.creavo.in/api/frame/category/count", timeout=5)
            counts = resp.json() if resp.status_code == 200 else {}
        except Exception:
            counts = {}
        print(counts)
        # Add count field to each frametype
        data = []
        for item in serializer.data:
            name = item.get('name')
            item['count'] = counts.get(name, 0)
            data.append(item)

        return Response(data)