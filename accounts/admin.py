from django.contrib import messages
from django.urls import path
from django.contrib import admin
from django.shortcuts import get_object_or_404, redirect
from .models import User, Subscription, License, Distributor, MasterDistributor, Order, OrderSubscription

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'mobile_number', 'is_verified', 'date_joined')
    search_fields = ('email', 'mobile_number', 'first_name', 'last_name')
    list_filter = ('is_verified', 'date_joined')

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