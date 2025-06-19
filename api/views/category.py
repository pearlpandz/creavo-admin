from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from accounts.permissions import IsAuthenticated
from api.serializers.category import CategorySerializer
from api.serializers.subcategory import SubCategorySerializer
from api.models.category import Category
from drf_spectacular.utils import extend_schema, OpenApiParameter # type: ignore
from api.serializers.media import GetMediaSerializer

@extend_schema(tags=['Cateogry'])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        parameters=[
            OpenApiParameter(name='limit', description='Number of items to return', required=False, type=int, default=15),
            OpenApiParameter(name='skip', description='Number of items to skip', required=False, type=int, default=0),
        ]
    )
    @action(detail=False, methods=['get'], url_path='list')
    def category_paginate(self, request):
        """
        Returns list of category, with pagination.
        Query params:
            limit: int
            skip: int
        """
        limit = int(request.GET.get('limit', 15))
        skip = int(request.GET.get('skip', 0))
        queryset = Category.objects.all()
        total = queryset.count()
        categories = queryset[skip:skip+limit]
        data = {
            'categories': CategorySerializer(categories, many=True, context={'request': request}).data,
            'total': total,
            'limit': limit,
            'skip': skip
        }
        return Response(data)

    @extend_schema(
        parameters=[
            OpenApiParameter(name='subcategoryid', description='Subcategory ID or "all"', required=False, type=str),
            OpenApiParameter(name='limit', description='Number of items to return', required=False, type=int, default=15),
            OpenApiParameter(name='skip', description='Number of items to skip', required=False, type=int, default=0),
        ]
    )
    @action(detail=True, methods=['get'], url_path='media_list')
    def media_list(self, request, pk=None):
        """
        Returns media for a category, filtered by subcategory, with pagination.
        Query params:
            subcategoryid: int or 'all'
            limit: int
            skip: int
        """
        category = self.get_object()
        subcategory_id = request.GET.get('subcategoryid')
        limit = int(request.GET.get('limit', 15))
        skip = int(request.GET.get('skip', 0))
        media_qs = category.media.all()
        if subcategory_id and subcategory_id != 'all':
            media_qs = media_qs.filter(subcategories__id=subcategory_id)
        total = media_qs.count()
        media = media_qs[skip:skip+limit]
        data = {
            # 'category': CategorySerializer(category).data,
            'media': GetMediaSerializer(media, many=True, context={'request': request}).data,
            'total': total,
            'limit': limit,
            'skip': skip
        }
        return Response(data)
    
@extend_schema(tags=['Subcateogry'])
class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        parameters=[
            OpenApiParameter(name='limit', description='Number of items to return', required=False, type=int, default=15),
            OpenApiParameter(name='skip', description='Number of items to skip', required=False, type=int, default=0),
        ]
    )
    @action(detail=False, methods=['get'], url_path='list')
    def category_paginate(self, request):
        """
        Returns list of category, with pagination.
        Query params:
            limit: int
            skip: int
        """
        limit = int(request.GET.get('limit', 15))
        skip = int(request.GET.get('skip', 0))
        queryset = Category.objects.all()
        total = queryset.count()
        categories = queryset[skip:skip+limit]
        data = {
            'categories': SubCategorySerializer(categories, many=True, context={'request': request}).data,
            'total': total,
            'limit': limit,
            'skip': skip
        }
        return Response(data)
    