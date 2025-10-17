from django.contrib import admin
from .models import (ContactInquiry, NewsletterSubscriber, MediaLibrary,
                     PageSection, Project, Service, ServiceFeature,
                     Template, TemplateCategory, Testimonial, SiteSetting)

admin.site.register(ContactInquiry)
admin.site.register(NewsletterSubscriber)
admin.site.register(MediaLibrary)
admin.site.register(PageSection)
admin.site.register(Project)
admin.site.register(Service)
admin.site.register(ServiceFeature)
admin.site.register(Template)
admin.site.register(TemplateCategory)
admin.site.register(Testimonial)
admin.site.register(SiteSetting)
