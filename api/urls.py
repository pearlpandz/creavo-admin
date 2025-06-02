from rest_framework.routers import DefaultRouter
from .views.event import EventViewSet
from api.views.media import MediaViewSet
from api.views.event import EventViewSet
from api.views.category import CategoryViewSet

router = DefaultRouter()
router.register(r'media', MediaViewSet, basename='media')
router.register(r'events', EventViewSet, basename='event')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
     
]

urlpatterns += router.urls