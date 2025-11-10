from rest_framework import serializers

from api.serializers.subcategory import SubCategorySerializer
from ..models.user import User, CompanyDetails, Product, Political, Supporters, Party
from ..serializers.license import LicenseSerializer
from ..serializers.subscription import SubscriptionSerializer

from rest_framework import serializers
from ..models.user import User
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate_email(self, value):
        """Check if email already exists."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists!")
        return value

    def validate_mobile_number(self, value):
        """Check if mobile number is valid and unique."""
        if not re.fullmatch(r'^[6-9]\d{9}$', value):  # basic Indian mobile number validation
            raise serializers.ValidationError("Mobile number must be a valid 10-digit number.")
        if User.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError("Mobile number already exists!")
        return value

    def create(self, validated_data):
        """Hash password and create the user."""
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = '__all__'

class SupportersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supporters
        fields = '__all__'

class PoliticalSerializer(serializers.ModelSerializer):
    supporters = SupportersSerializer(many=True)
    party = PartySerializer(many=True)
    class Meta:
        model = Political
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def validate(self, data):
        user = data.get("user") or getattr(self.instance, "user", None)
        if user:
            existing_count = Product.objects.filter(user=user).exclude(id=self.instance.id if self.instance else None).count()
            if not self.instance and existing_count >= 6:
                raise serializers.ValidationError("Maximum 6 products allowed per user.")
            if self.instance and existing_count >= 6:
                raise serializers.ValidationError("User already has 6 products — cannot assign more.")
        return data


class CompanyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDetails
        fields = "__all__"

class UserDetailSerializer(serializers.ModelSerializer):
    company_details = CompanyDetailsSerializer()
    political = PoliticalSerializer()
    products = serializers.SerializerMethodField()  
    business_category = SubCategorySerializer(many=True)
    language = SubCategorySerializer(many=True)

    class Meta:
        model = User
        exclude = ['password']

    def get_products(self, obj):
        """Return only valid products — never null-filled ones."""
        products = obj.products.all().exclude(
            name__isnull=True,
            image__isnull=True,
            media__isnull=True
        )
        if not products.exists():
            return []
        return ProductSerializer(products, many=True).data
