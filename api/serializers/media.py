from rest_framework import serializers
from api.models.media import Media

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'

# This serializer used only for get list of media under category or subcategory api
class GetMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        exclude = ['categories', 'subcategories']
