from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PhoneOTP

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role','phone_number','phone_verified','parent','created_by')}),
    )

@admin.register(PhoneOTP)
class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ('phone','otp','created_at','attempts')
