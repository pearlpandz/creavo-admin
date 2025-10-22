from django.db import models
from django.utils import timezone

class ContactInquiry(models.Model):
    STATUS_CHOICES = [('new','new'),('read','read'),('replied','replied'),('archived','archived')]
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(default=timezone.now)

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(default=timezone.now)

class MediaLibrary(models.Model):
    file_name = models.CharField(max_length=512)
    file_path = models.CharField(max_length=1024)  # or use FileField
    file_type = models.CharField(max_length=100)
    file_size = models.BigIntegerField()
    alt_text = models.CharField(max_length=512, blank=True, default='')
    uploaded_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def url(self):
        # assuming MEDIA_URL + basename
        import os
        from django.conf import settings
        return f"{settings.MEDIA_URL}{os.path.basename(self.file_path)}"

class PageSection(models.Model):
    page_name = models.CharField(max_length=255)
    section_name = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    content_type = models.CharField(max_length=50, default='html')
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

class Project(models.Model):
    title = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image_url = models.CharField(max_length=1024, blank=True, null=True)
    project_url = models.CharField(max_length=1024, blank=True, null=True)
    technologies_used = models.CharField(max_length=1024, blank=True, null=True)
    completion_date = models.DateField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

class Service(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=255, blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    image_url = models.CharField(max_length=1024, blank=True, null=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

class ServiceFeature(models.Model):
    service = models.ForeignKey(Service, related_name='features', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=255, blank=True, null=True)
    display_order = models.IntegerField(default=0)

class TemplateCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

class Template(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(TemplateCategory, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image_url = models.CharField(max_length=1024, blank=True, null=True)
    preview_url = models.CharField(max_length=1024, blank=True, null=True)
    download_url = models.CharField(max_length=1024, blank=True, null=True)
    tags = models.CharField(max_length=1024, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    downloads_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

class Testimonial(models.Model):
    client_name = models.CharField(max_length=255)
    client_position = models.CharField(max_length=255, blank=True, null=True)
    client_company = models.CharField(max_length=255, blank=True, null=True)
    client_image = models.CharField(max_length=1024, blank=True, null=True)
    testimonial_text = models.TextField()
    rating = models.IntegerField(default=5)
    is_featured = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

class SiteSetting(models.Model):
    setting_key = models.CharField(max_length=255, unique=True)
    setting_value = models.TextField()
    setting_type = models.CharField(max_length=50, default='text')


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    short_description = models.TextField(blank=True, null=True)
    content = models.TextField()
    feature_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    author_name = models.CharField(max_length=100, default='Admin')
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)