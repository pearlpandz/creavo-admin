from rest_framework.routers import DefaultRouter
from .views.event import EventViewSet
from api.views.media import MediaViewSet
from api.views.event import EventViewSet
from api.views.category import CategoryViewSet, SubCategoryViewSet

router = DefaultRouter()
router.register(r'media', MediaViewSet, basename='media')
router.register(r'events', EventViewSet, basename='event')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'subcategories', SubCategoryViewSet, basename='subcategory')

urlpatterns = [
     
]

urlpatterns += router.urls