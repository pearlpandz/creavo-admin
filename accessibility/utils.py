from .models import RoleEntitlement

def user_has_entitlement(user, entitlement_name):
    if user.is_superuser:
        return True
    return RoleEntitlement.objects.filter(role=user.role, entitlement__name=entitlement_name).exists()
