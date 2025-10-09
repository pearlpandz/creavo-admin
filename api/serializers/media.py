from rest_framework import serializers
from api.models.media import Media
from api.models.category import Category
from api.models.subcategory import SubCategory

class MediaSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True, required=False
    )
    subcategories = serializers.PrimaryKeyRelatedField(
         queryset=SubCategory.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Media
        fields = '__all__'
        
    def validate_media(self, value):
        allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov']
        ext = value.name.split('.')[-1].lower()
        if ext not in allowed_extensions:
            raise serializers.ValidationError("Unsupported file type.")
        return value

# This serializer used only for get list of media under category or subcategory api
class GetMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        exclude = ['categories', 'subcategories']
