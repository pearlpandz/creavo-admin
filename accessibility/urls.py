from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EntitlementViewSet, RoleEntitlementViewSet, my_entitlements, has_access

router = DefaultRouter()
router.register(r'entitlements', EntitlementViewSet, basename='entitlement')
router.register(r'role-entitlements', RoleEntitlementViewSet, basename='role-entitlement')

urlpatterns = [
    path('', include(router.urls)),
    path('my-entitlements/', my_entitlements, name='my_entitlements'),
    path('has-access/<str:entitlement_name>/', has_access, name='has_access'),
]
