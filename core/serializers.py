from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from accessibility.models import RoleEntitlement

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','first_name','last_name','role','phone_number','phone_verified','parent','created_by']

class ProfileSerializer(UserSerializer):
    entitlements = serializers.SerializerMethodField()
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['entitlements']

    def get_entitlements(self, obj):
        items = RoleEntitlement.objects.filter(role=obj.role).select_related('entitlement')
        return [i.entitlement.name for i in items]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','email','password','first_name','last_name','role','phone_number']

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated):
        user = User.objects.create_user(
            username=validated['username'],
            email=validated['email'],
            password=validated['password'],
            first_name=validated.get('first_name',''),
            last_name=validated.get('last_name',''),
            role=validated.get('role','retailer'),
        )
        user.is_active = False
        user.phone_number = validated.get('phone_number')
        user.save()
        return user

class ProfilePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','phone_number']
