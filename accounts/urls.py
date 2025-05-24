from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.order import OrderViewSet
from .views.master_distributor import MasterDistributorViewSet
from .views.distributor import DistributorViewSet
from .views.user import UserViewSet
from .views.subscription import SubscriptionViewSet
from .views.license import LicenseViewSet, licenses_by_distributor, licenses_by_master_distributor
from .views.license_generator import LicenseGeneratorAPIView
from .views.authentication import UserAuthenticationAPIView, DistributorAuthenticationAPIView, MasterDistributorAuthenticationAPIView

router = DefaultRouter()
router.register(r'master-distributors', MasterDistributorViewSet, basename='master-distributor')
router.register(r'distributors', DistributorViewSet, basename='distributor')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'orders', OrderViewSet, basename='order') 
router.register(r'licenses', LicenseViewSet, basename='license')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('generate-licenses/', LicenseGeneratorAPIView.as_view(), name='generate-licenses'),
    path('licenses/distributor/<int:distributor_id>/', licenses_by_distributor, name='licenses-by-distributor'),
    path('licenses/master-distributor/<int:master_distributor_id>/', licenses_by_master_distributor, name='licenses-by-master-distributor'),
]

urlpatterns += router.urls

urlpatterns += [
    path('auth/user/', UserAuthenticationAPIView.as_view(), name='user-authentication'),
    path('auth/distributor/', DistributorAuthenticationAPIView.as_view(), name='distributor-authentication'),
    path('auth/master-distributor/', MasterDistributorAuthenticationAPIView.as_view(), name='master-distributor-authentication'),
]