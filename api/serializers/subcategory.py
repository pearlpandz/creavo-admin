from rest_framework import serializers
from api.models.subcategory import SubCategory
from api.serializers.media import GetMediaSerializer
from api.models.media import Media

# This serializer used only for get list of subcategory under category api
class SubCategorySerializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField()
    media_count = serializers.SerializerMethodField()
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'description','media_count']
        exclude = ['category']

    def create(self, validated_data):
        media_data = validated_data.pop('media', [])
        subcategory = SubCategory.objects.create(**validated_data)
        for media_item in media_data:
            Media.objects.create(subcategories=[subcategory], **media_item)
        return subcategory

    def update(self, instance, validated_data):
        media_data = validated_data.pop('media', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        for media_item in media_data:
            Media.objects.create(subcategories=[instance], **media_item)
        return instance
