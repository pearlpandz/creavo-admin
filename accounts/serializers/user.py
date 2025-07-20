from rest_framework import serializers

from api.serializers.subcategory import SubCategorySerializer
from ..models.user import User, CompanyDetails, Product, Political, Supporters, Party
from ..serializers.license import LicenseSerializer
from ..serializers.subscription import SubscriptionSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

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

class CompanyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDetails
        fields = "__all__"

class UserDetailSerializer(serializers.ModelSerializer):
    company_details = CompanyDetailsSerializer()
    political = PoliticalSerializer()
    products = ProductSerializer(many=True)
    business_category = SubCategorySerializer(many=True)
    language = SubCategorySerializer(many=True)

    class Meta:
        model = User
        exclude = ['password']
