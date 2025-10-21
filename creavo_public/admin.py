# from django.contrib import admin
# from .models import (ContactInquiry, NewsletterSubscriber, MediaLibrary,
#                      PageSection, Project, Service, ServiceFeature,
#                      Template, TemplateCategory, Testimonial, SiteSetting)

# admin.site.register(ContactInquiry)
# admin.site.register(NewsletterSubscriber)
# admin.site.register(MediaLibrary)
# admin.site.register(PageSection)
# admin.site.register(Project)
# admin.site.register(Service)
# admin.site.register(ServiceFeature)
# admin.site.register(Template)
# admin.site.register(TemplateCategory)
# admin.site.register(Testimonial)
# admin.site.register(SiteSetting)

from .models import  Blog
from django.utils.html import format_html
from django.contrib import admin
from .models import (
    ContactInquiry,
    NewsletterSubscriber,
    MediaLibrary,
    PageSection,
    Project,
    Service,
    ServiceFeature,
    Template,
    TemplateCategory,
    Testimonial,
    SiteSetting
)


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    ordering = ('-created_at',)


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_active', 'subscribed_at')
    list_filter = ('is_active',)
    search_fields = ('email',)
    ordering = ('-subscribed_at',)


@admin.register(MediaLibrary)
class MediaLibraryAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name', 'file_type', 'file_size', 'uploaded_by', 'created_at')
    search_fields = ('file_name', 'file_type', 'uploaded_by')
    list_filter = ('file_type', 'created_at')
    ordering = ('-created_at',)


@admin.register(PageSection)
class PageSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'page_name', 'section_name', 'is_active', 'display_order', 'updated_at')
    list_filter = ('page_name', 'is_active')
    search_fields = ('page_name', 'section_name', 'content')
    ordering = ('page_name', 'display_order')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'client_name', 'category', 'is_active', 'is_featured')
    list_filter = ('category', 'is_active', 'is_featured')
    search_fields = ('title', 'client_name', 'category')
    ordering = ('display_order',)


class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured')
    search_fields = ('title', 'slug', 'description')
    inlines = [ServiceFeatureInline]
    ordering = ('display_order',)


@admin.register(TemplateCategory)
class TemplateCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'is_active')
    search_fields = ('name', 'slug')
    ordering = ('display_order',)


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'is_active', 'is_featured', 'downloads_count')
    list_filter = ('is_active', 'is_featured', 'category')
    search_fields = ('name', 'description', 'tags')
    ordering = ('-created_at',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'client_company', 'rating', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured', 'rating')
    search_fields = ('client_name', 'client_company', 'testimonial_text')
    ordering = ('display_order',)


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('setting_key', 'setting_type', 'short_value')
    search_fields = ('setting_key',)
    list_filter = ('setting_type',)
    ordering = ('setting_key',)

    def short_value(self, obj):
        val = obj.setting_value
        return val[:50] + '...' if len(val) > 50 else val
    short_value.short_description = 'Value'

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author_name', 'is_featured', 'is_active', 'image_preview', 'published_at')
    list_filter = ('is_featured', 'is_active', 'published_at')
    search_fields = ('title', 'content', 'author_name')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views',)
    ordering = ('-published_at',)

    def image_preview(self, obj):
        if obj.feature_image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:4px;" />', obj.feature_image.url)
        return "-"
    image_preview.short_description = 'Image Preview'


