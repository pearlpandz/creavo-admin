from rest_framework import serializers
from ..models.master_distributor import MasterDistributor

class MasterDistributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterDistributor
        fields = '__all__'
