from typing import List
from rest_framework import serializers
from accounts.models.license import License
from accounts.models.user import User
from accounts.serializers.license import LicenseSerializer
from accounts.serializers.user import UserDetailSerializer
from accounts.utils import get_user_from_access_token
from api.models.category import Category
from api.models.subcategory import SubCategory
from api.serializers.subcategory import SubCategorySerializer

# This serializer used only for get categories along with its subcategory api
class CategorySerializer(serializers.ModelSerializer):
    # subcategories = SubCategorySerializer(many=True, read_only=True)
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_subcategories(self, category) -> List[SubCategorySerializer]:
        request = self.context.get('request')
        user = get_user_from_access_token(request, User)

        # extracting user details
        profile = UserDetailSerializer(user).data

        category_name = category.name.lower()

        # Handle Business Category
        if category_name == 'business category':
            business_categories = profile.get('business_category', [])
            allowed_ids = [item['id'] for item in business_categories]
            return SubCategorySerializer(
                SubCategory.objects.filter(id__in=allowed_ids, category=category),
                many=True,
                context=self.context
            ).data

        # Handle Language
        elif category_name == 'language':
            languages = profile.get('language', [])
            allowed_ids = [item['id'] for item in languages]
            return SubCategorySerializer(
                SubCategory.objects.filter(id__in=allowed_ids, category=category),
                many=True,
                context=self.context
            ).data

        # Default: empty or all subcategories if needed
        return SubCategorySerializer(
            SubCategory.objects.filter(category=category),
            many=True,
            context=self.context
        ).data


