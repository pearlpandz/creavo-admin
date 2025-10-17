from rest_framework import serializers
from .models import (ContactInquiry, NewsletterSubscriber, MediaLibrary,
                     PageSection, Project, Service, ServiceFeature,
                     Template, TemplateCategory, Testimonial, SiteSetting)

class ContactInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInquiry
        fields = '__all__'
        read_only_fields = ('status','created_at')

class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = '__all__'
        read_only_fields = ('subscribed_at',)

class MediaLibrarySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    class Meta:
        model = MediaLibrary
        fields = ['id','file_name','file_path','file_type','file_size','alt_text','uploaded_by','created_at','url']
    def get_url(self, obj):
        return obj.url()

class PageSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageSection
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ServiceFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceFeature
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    features = ServiceFeatureSerializer(many=True, read_only=True)
    class Meta:
        model = Service
        fields = '__all__'

class TemplateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateCategory
        fields = '__all__'

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

class SiteSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSetting
        fields = ['setting_key','setting_value','setting_type']
