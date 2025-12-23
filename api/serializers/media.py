from rest_framework import serializers
from api.models.media import Media
from api.models.category import Category
from api.models.subcategory import SubCategory

class MediaSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True, required=False
    )
    subcategories = serializers.PrimaryKeyRelatedField(
            queryset=SubCategory.objects.all(), many=True, required=False
    )

    class Meta:
        model = Media
        fields = '__all__'
        
    def validate_media(self, value):
        allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov']
        ext = value.name.split('.')[-1].lower()
        if ext not in allowed_extensions:
            raise serializers.ValidationError("Unsupported file type.")
        
        size = value.size
        if ext in ['jpg', 'jpeg', 'png']:
            max_size = 2 * 1024 * 1024  # 2 MB
        elif ext == 'gif':
            max_size = 5 * 1024 * 1024  # 5 MB
        elif ext in ['mp4', 'mov']:
            max_size = 5 * 1024 * 1024  # 5 MB
        else:
            max_size = 2 * 1024 * 1024  # default 2 MB

        if size > max_size:
            raise serializers.ValidationError(f"File too large. Maximum allowed size for {ext.upper()} is {max_size // (1024*1024)} MB.")

        return value

    def create(self, validated_data):
        categories = validated_data.pop('categories', [])
        subcategories = validated_data.pop('subcategories', [])
        instance = Media.objects.create(**validated_data)
        if categories:
            instance.categories.set(categories)
        if subcategories:
            instance.subcategories.set(subcategories)
        return instance

    def update(self, instance, validated_data):
        categories = validated_data.pop('categories', None)
        subcategories = validated_data.pop('subcategories', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if categories is not None:
            instance.categories.set(categories)
        if subcategories is not None:
            instance.subcategories.set(subcategories)
        return instance

# This serializer used only for get list of media under category or subcategory api
class GetMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        exclude = ['categories', 'subcategories']


class BulkMediaUploadSerializer(serializers.Serializer):
    media = serializers.ListField(
        child=serializers.FileField(),
        required=True
    )


    def create(self, validated_data):
        return validated_data

