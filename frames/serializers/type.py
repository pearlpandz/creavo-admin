from rest_framework import serializers
from frames.models.type import FrameType
from api.serializers.subcategory import SubCategorySerializer

class FrameTypeSerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = FrameType
        exclude = ['media']
