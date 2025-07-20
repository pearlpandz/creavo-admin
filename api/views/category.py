from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from accounts.models.license import License
from accounts.models.user import User
from accounts.permissions import IsAuthenticated
from accounts.serializers.license import LicenseSerializer
from accounts.serializers.user import UserDetailSerializer
from accounts.utils import get_user_from_access_token
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
        user = get_user_from_access_token(request, User)

        # extracting license details along with associated subscription details
        license = License.objects.filter(purchased_by=user).first()
        license_details = LicenseSerializer(license).data if license else None
        subscription = license_details.get('subscription')
        show_trending = subscription.get('show_trending', False)

        limit = int(request.GET.get('limit', 15))
        skip = int(request.GET.get('skip', 0))
        queryset = Category.objects.all()

        if not show_trending:
            queryset = queryset.exclude(name__iexact='trending')

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
        user = get_user_from_access_token(request, User)
        # extracting license details along with associated subscription details
        license = License.objects.filter(purchased_by=user).first()
        license_details = LicenseSerializer(license).data if license else None

        category = self.get_object()
        subcategory_id = request.GET.get('subcategoryid')
        limit = int(request.GET.get('limit', 15))
        skip = int(request.GET.get('skip', 0))
        media_qs = category.media.all()

        subscription = license_details.get('subscription', None)
        enabled_ratings = subscription.get('enabled_ratings', [])

        if subcategory_id and subcategory_id != 'all':
            media_qs = media_qs.filter(subcategories__id=subcategory_id)
        
        if license_details is None:
            media_qs = media_qs.filter(rating__in=[5])
        else:
            # filter based on subscription specific ratings based media
            media_qs = media_qs.filter(rating__in=enabled_ratings)
        
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
    