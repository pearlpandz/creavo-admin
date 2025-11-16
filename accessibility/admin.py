from django.contrib import admin
from .models import Entitlement, RoleEntitlement

@admin.register(Entitlement)
class EntitlementAdmin(admin.ModelAdmin):
    list_display = ('name','description')

@admin.register(RoleEntitlement)
class RoleEntitlementAdmin(admin.ModelAdmin):
    list_display = ('role','entitlement')
