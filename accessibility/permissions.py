from rest_framework.permissions import BasePermission
from .models import RoleEntitlement

class HasEntitlement(BasePermission):
    def __init__(self, entitlement_name=None):
        self.entitlement_name = entitlement_name

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return RoleEntitlement.objects.filter(role=request.user.role, entitlement__name=self.entitlement_name).exists()

def entitlement_required(name):
    return HasEntitlement(entitlement_name=name)
