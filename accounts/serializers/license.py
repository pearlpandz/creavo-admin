from rest_framework import serializers
from ..models.license import License
from ..models.subscription import Subscription
from ..models.distributor import Distributor
from ..models.master_distributor import MasterDistributor
from ..models.user import User

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'name']

class DistributorSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Distributor
        fields = ['id', 'name', 'email', 'mobile_number', 'created_at', 'is_verified']

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class MasterDistributorSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = MasterDistributor
        fields = ['id', 'name']

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'mobile_number', 'date_joined', 'is_verified', 'downloads', 'exceeded_downloads', 'no_subscription_downloads']

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class LicenseSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer()
    issued_to_distributor = DistributorSerializer()
    issued_to_master_distributor = MasterDistributorSerializer()
    purchased_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.purchased_by:
            representation['purchased_by'] = {
                'id': instance.purchased_by.id,
                'name': f"{instance.purchased_by.first_name} {instance.purchased_by.last_name}"
            }
        return representation

    class Meta:
        model = License
        fields = '__all__'
