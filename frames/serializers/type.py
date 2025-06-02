from rest_framework import serializers
from frames.models.type import FrameType

class FrameTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrameType
        exclude = ['media']
