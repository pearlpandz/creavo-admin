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
        fields = ['id', 'name', 'description','media_count','category','media']
        # exclude = ['category']

    def get_media_count(self, obj):
        return obj.media.count()
    
    def get_media(self, obj):
        media_qs = obj.media.all()  # ✅ use the instance, not the class
        return GetMediaSerializer(media_qs, many=True, context=self.context).data

    def create(self, validated_data):
        media_data = validated_data.pop('media', [])
        subcategory = SubCategory.objects.create(**validated_data)
        for media_item in media_data:
            m = Media.objects.create(**media_item)
            m.subcategories.add(subcategory)
            if hasattr(subcategory, 'category') and subcategory.category:
                m.categories.add(subcategory.category)
        return subcategory

    def update(self, instance, validated_data):
        media_data = validated_data.pop('media', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        for media_item in media_data:
            m = Media.objects.create(**media_item)
            m.subcategories.add(instance)
            if hasattr(instance, 'category') and instance.category:
                m.categories.add(instance.category)
        return instance
