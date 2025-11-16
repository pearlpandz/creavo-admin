from rest_framework import serializers
from .models import Entitlement, RoleEntitlement

class EntitlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entitlement
        fields = ['id','name','description']

class RoleEntitlementSerializer(serializers.ModelSerializer):
    entitlement = EntitlementSerializer(read_only=True)
    entitlement_id = serializers.PrimaryKeyRelatedField(queryset=Entitlement.objects.all(), source='entitlement', write_only=True)

    class Meta:
        model = RoleEntitlement
        fields = ['role','entitlement','entitlement_id']
