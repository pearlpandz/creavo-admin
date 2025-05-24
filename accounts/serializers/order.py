from rest_framework import serializers
from ..models.order import Order, OrderSubscription

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderSubscription
        fields = '__all__'
