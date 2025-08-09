
from rest_framework import serializers
from api.models.event import Event
from api.models.event import EventMedia
class EventMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventMedia
        fields = ['id', 'media', 'image', 'media_type']

class EventSerializer(serializers.ModelSerializer):
    images = EventMediaSerializer(source='events', many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'name', 'date', 'images']

