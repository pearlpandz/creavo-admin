from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ContactViewSet, NewsletterViewSet, MediaViewSet, PageSectionViewSet,
                    ProjectViewSet, ServiceViewSet, TemplateViewSet, TemplateCategoryViewSet,
                    TestimonialViewSet, SettingsViewSet)
from .views import CMSPageAPI
router = DefaultRouter()
router.register(r'contact', ContactViewSet, basename='contact')
router.register(r'newsletter', NewsletterViewSet, basename='newsletter')
# media is custom ViewSet
from .views import MediaViewSet
media_list = MediaViewSet.as_view({'get':'list','post':'create'})
media_detail = MediaViewSet.as_view({'get':'retrieve','delete':'destroy'})
# resourceful viewsets
router.register(r'projects', ProjectViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'templates', TemplateViewSet)
router.register(r'template-categories', TemplateCategoryViewSet)
router.register(r'testimonials', TestimonialViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('media/', media_list, name='media-list'),
    path('media/<int:pk>/', media_detail, name='media-detail'),
    path('pages/', PageSectionViewSet.as_view({'get':'list'}), name='pages-list'),
    path('pages/<str:pk>/', PageSectionViewSet.as_view({'get':'retrieve'}), name='pages-detail'),
    path('settings/', SettingsViewSet.as_view({'get':'list'}), name='settings-list'),
    path('settings/<str:pk>/', SettingsViewSet.as_view({'get':'retrieve','put':'update'}), name='settings-detail'),
    path("cms/", CMSPageAPI.as_view(), name="cms_page_api"),
]
