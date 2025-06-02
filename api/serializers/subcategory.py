from rest_framework import serializers
from api.models.subcategory import SubCategory


# This serializer used only for get list of subcategory under category api
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        exclude = ['category']
