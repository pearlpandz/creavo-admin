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
from api.serializers.category import BaseCategorySerializer, CategorySerializer
from api.serializers.subcategory import SubCategorySerializer
from api.models.category import Category
from api.models.subcategory import SubCategory
from drf_spectacular.utils import extend_schema, OpenApiParameter # type: ignore
from api.serializers.media import GetMediaSerializer

@extend_schema(tags=['Cateogry'])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'signup_list':
            return BaseCategorySerializer
        return super().get_serializer_class()
    
    @action(detail=False, methods=["get"], url_path="signup-list")
    def signup_list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
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
        show_trending = False
        if license_details is not None:
            subscription = license_details.get('subscription')
            show_trending = subscription.get('show_trending', False)

        limit = int(request.GET.get('limit', 15))
        skip = int(request.GET.get('skip', 0))
        queryset = Category.objects.filter(is_active=True).order_by('order', 'name')

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
        if subcategory_id != 'all' and subcategory_id != None:
            media_qs = category.media.filter(subcategories__id=int(subcategory_id))
        enabled_ratings = []
        if license_details is not None:
            subscription = license_details.get('subscription', None)
            enabled_ratings = subscription.get('enabled_ratings', [])

        # Only apply subcategory filter logic for 'business' or 'language' categories
        if "business" in category.name.lower():
            if subcategory_id and subcategory_id != 'all':
                if str(subcategory_id).isdigit():
                    media_qs = media_qs.filter(subcategories__id=int(subcategory_id))
            elif subcategory_id == 'all':
                ids = user.business_category.values_list("id", flat=True)
                media_qs = media_qs.filter(subcategories__id__in=ids)
        elif "language" in category.name.lower():
            if subcategory_id and subcategory_id != 'all':
                if str(subcategory_id).isdigit():
                    media_qs = media_qs.filter(subcategories__id=int(subcategory_id))
            elif subcategory_id == 'all':
                ids = user.language.values_list("id", flat=True)
                media_qs = media_qs.filter(subcategories__id__in=ids)
        # For other categories, do not filter by subcategory at all (always return all media)

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
    # queryset = Category.objects.all()
    queryset =  SubCategory.objects.filter(is_active=True)
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
    