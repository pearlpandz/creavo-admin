from rest_framework import serializers
from ..models.distributor import Distributor
from ..models.master_distributor import MasterDistributor

class MasterDistributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterDistributor
        fields = ['id', 'first_name', 'last_name']

class DistributorSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=MasterDistributor.objects.all())
    verified_by = serializers.StringRelatedField()

    class Meta:
        model = Distributor
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.created_by:
            representation['created_by'] = {
                'id': instance.created_by.id,
                'first_name': instance.created_by.first_name,
                'last_name': instance.created_by.last_name
            }
        return representation
