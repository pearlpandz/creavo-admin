from rest_framework import serializers
from api.models.category import Category
from api.serializers.subcategory import SubCategorySerializer

# This serializer used only for get categories along with its subcategory api
class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


