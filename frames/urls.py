from .views.type import FrameTypeViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'frametypes', FrameTypeViewSet, basename='frametypes')

urlpatterns = [
     
]

urlpatterns += router.urls