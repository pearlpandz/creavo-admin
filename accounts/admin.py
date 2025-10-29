from django.contrib import messages
from django.urls import path
from django.contrib import admin
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import ValidationError
import re
from api.models.category import Category
from api.models.subcategory import SubCategory
from .models import User, Subscription, License, Distributor, MasterDistributor, Order, OrderSubscription, CompanyDetails, Product, Political, Supporters, Party
import nested_admin

class ProductInline(nested_admin.NestedTabularInline):
    model = Product
    extra = 0

    def clean(self):
        super().clean()
        if any(self.errors):
            return
        total_forms = len([form for form in self.forms if not form.cleaned_data.get('DELETE', False)])
        existing_count = Product.objects.filter(user=self.instance).count()
        if total_forms + existing_count > 6:
            raise ValidationError("A user can have a maximum of 6 products.")

class CompanyDetailsInline(nested_admin.NestedStackedInline):
    model = CompanyDetails
    extra = 0
    exclude = ['image']  # hides the field from the form

class SupportersInline(nested_admin.NestedTabularInline):
    model = Supporters
    extra = 0
    exclude = ['image']  # hides the field from the form

class PartyInline(nested_admin.NestedTabularInline):
    model = Party
    extra = 0
    exclude = ['image']  # hides the field from the form

class PoliticalInline(nested_admin.NestedStackedInline):
    model = Political
    extra = 0
    exclude = ['image']  # hides the field from the form
    inlines = [PartyInline, SupportersInline]


# forms.py
from django import forms
from .models import User, Category, SubCategory

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Email already exists!")
        return email

    def clean_mobile_number(self):
        mobile = self.cleaned_data.get('mobile_number')
        if not re.fullmatch(r'^[6-9]\d{9}$', mobile):
            raise ValidationError("Mobile number must be a valid 10-digit number.")
        if User.objects.filter(mobile_number=mobile).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Mobile number already exists!")
        return mobile

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # For business_category field
        business_parent = Category.objects.filter(name='Business Category').first()
        if 'business_category' in self.fields:
            if business_parent:
                self.fields['business_category'].queryset = SubCategory.objects.filter(category=business_parent)
            else:
                self.fields['business_category'].queryset = SubCategory.objects.none()

        # For language field
        language_parent = Category.objects.filter(name='Language').first()
        if 'language' in self.fields:
            if language_parent:
                self.fields['language'].queryset = SubCategory.objects.filter(category=language_parent)
            else:
                self.fields['language'].queryset = SubCategory.objects.none()

@admin.register(User)
class UserAdmin(nested_admin.NestedModelAdmin):
    form = UserAdminForm 
    list_display = ('first_name', 'last_name', 'email', 'mobile_number', 'date_joined')
    search_fields = ('email', 'mobile_number', 'first_name', 'last_name')
    list_filter = ['date_joined']
    inlines = [CompanyDetailsInline, ProductInline, PoliticalInline]
    
    
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')

@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('code', 'subscription', 'issued_to_distributor', 'issued_to_master_distributor', 'created_at', 'status')
    search_fields = ('code',)
    list_filter = ('created_at', 'subscription')

@admin.register(Distributor)
class DistributorAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name', 'email', 'mobile_number')
    search_fields = ('first_name','last_name', 'email', 'mobile_number')

@admin.register(MasterDistributor)
class MasterDistributorAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name', 'email', 'mobile_number')
    search_fields = ('first_name','last_name', 'email', 'mobile_number')

class OrderSubscriptionInline(admin.TabularInline):
    model = OrderSubscription
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'master_distributor_id', 'distributor_id', 'subtotal', 'discount', 'total', 'status', 'created_at')
    inlines = [OrderSubscriptionInline]
    change_form_template = 'admin/orders/change_form.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:order_id>/approve/', self.admin_site.admin_view(self.process_approval), name='order-approve'),
        ]
        return custom_urls + urls

    def process_approval(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        
        if order.status == 'executed':
            self.message_user(request, "Order is already executed.", level=messages.WARNING)
            return redirect(f'../../{order_id}/change/')

        # Call your license generation logic here
        generate_license(order)  # Your function

        order.status = 'executed'
        order.save()
        self.message_user(request, "License generated and order marked as executed.")
        return redirect(f'../../{order_id}/change/')

def generate_license(order):
    for order_sub in order.subscriptions.all():
        for _ in range(order_sub.quantity):
            License.objects.create(
                subscription=order_sub.subscription,
                issued_to_master_distributor=order.master_distributor_id if order.master_distributor_id else None,
                issued_to_distributor=order.distributor_id if order.distributor_id else None,
                status='pending'
            )