from rest_framework import serializers
from api.models.media import Media

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'
