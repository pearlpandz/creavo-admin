from rest_framework.routers import DefaultRouter
from .views.event import EventViewSet
from api.views.media import MediaViewSet
from api.views.event import EventViewSet

router = DefaultRouter()
router.register(r'media', MediaViewSet, basename='media')
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
     
]

urlpatterns += router.urls