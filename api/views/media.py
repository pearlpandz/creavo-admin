from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from accounts.permissions import IsAuthenticated
from rest_framework import viewsets

from api.models.category import Category
from api.models.subcategory import SubCategory
from api.models.media import Media
from api.serializers.media import MediaSerializer
from drf_spectacular.utils import extend_schema # type: ignore

@extend_schema(tags=['Media'])
class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='grouped', url_name='grouped')
    def grouped(self, request):

        grouped = []

        categories = Category.objects.all().order_by('order', 'id')

        for category in categories:
            cat_data = {
                "category": category.name,                
                "subcategories": []
            }

            # Check if subcategories exist for the category
            media_items = Media.objects.filter(categories=category).distinct()[:10]  # limit to 10 items
            # If no subcategories, include media at the root level of the category
            if not SubCategory.objects.filter(category=category).exists():
                cat_data["media"] = [
                    {
                        "id": item.id,
                        "title": item.title,
                        "image": item.image
                    }
                    for item in media_items
                ]
                
            subcategories = SubCategory.objects.filter(category=category).order_by('name')

            for subcategory in subcategories:
                media_items = Media.objects.filter(
                    categories=category,
                    subcategories=subcategory
                ).distinct()[:10]  # limit to 10 items

                cat_data["subcategories"].append({
                    "name": subcategory.name,
                    "media": [
                        {
                            "id": item.id,
                            "title": item.title,
                            "image": item.image

                        }
                        for item in media_items 
                    ]
                })

            grouped.append(cat_data)

        return Response(grouped)
