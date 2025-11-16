from django.core.management.base import BaseCommand
from accessibility.models import Entitlement, RoleEntitlement

DEFAULT_ENTITLEMENTS = [
    ('view_retailer_dashboard','Retailer dashboard access'),
    ('view_distributor_portal','Distributor portal access'),
    ('create_order','Create orders'),
    ('manage_downline','Manage downline distributors'),
    ('view_reports','View reports'),
    # Expanded sample entitlements (add as needed)
    ('create_user','Create user'),
    ('view_user','View user'),
    ('edit_user','Edit user'),
    ('delete_user','Delete user'),
    ('create_child_user','Create child user'),
    ('view_children','View children'),
    ('transfer_user_between_parents','Transfer user between parents'),
    ('view_master_distributor','View master distributor'),
    ('edit_master_distributor','Edit master distributor'),
    ('create_master_distributor','Create master distributor'),
    ('delete_master_distributor','Delete master distributor'),
    ('view_super_master_distributor','View super master distributor'),
    ('edit_super_master_distributor','Edit super master distributor'),
    ('view_distributor','View distributor'),
    ('edit_distributor','Edit distributor'),
    ('create_distributor','Create distributor'),
    ('delete_distributor','Delete distributor'),
    ('view_retailer','View retailer'),
    ('edit_retailer','Edit retailer'),
    ('create_retailer','Create retailer'),
    ('delete_retailer','Delete retailer'),
    ('view_retailer_orders','View retailer orders'),
    ('create_retailer_orders','Create retailer orders'),
    ('view_order','View order'),
    ('edit_order','Edit order'),
    ('cancel_order','Cancel order'),
    ('view_order_history','View order history'),
    ('approve_order','Approve order'),
    ('export_orders','Export orders'),
    ('view_financial_reports','View financial reports'),
    ('export_reports','Export reports'),
    ('view_compliance_reports','View compliance reports'),
    ('manage_entitlements','Manage entitlements'),
    ('manage_role_entitlements','Manage role entitlements'),
    ('manage_system_settings','Manage system settings'),
    ('view_audit_logs','View audit logs'),
    ('manage_api_keys','Manage API keys'),
    ('change_password','Change password'),
    ('reset_password','Reset password'),
    ('verify_email','Verify email'),
    ('verify_phone','Verify phone'),
    ('update_profile','Update profile'),
    ('view_profile','View profile'),
    ('access_support','Access support'),
    ('view_notifications','View notifications'),
    ('manage_notifications','Manage notifications'),
    ('impersonate_user','Impersonate user'),
]

ROLE_MAP = {
    'retailer': ['view_retailer','create_retailer_orders','view_retailer_orders','update_profile','verify_phone','view_profile'],
    'distributor': ['view_retailer','create_retailer','view_children','create_order','view_reports','view_profile'],
    'master_distributor': ['view_retailer','create_retailer','view_children','create_order','manage_downline','edit_distributor','view_master_distributor','create_distributor','view_reports','view_profile'],
    'super_master_distributor': ['view_retailer','create_retailer','view_children','create_order','manage_downline','edit_distributor','view_master_distributor','create_distributor','manage_entitlements','view_audit_logs','view_reports','view_profile'],
}

class Command(BaseCommand):
    help = 'Seed default entitlements and role mappings'

    def handle(self, *args, **kwargs):
        for name, desc in DEFAULT_ENTITLEMENTS:
            Entitlement.objects.get_or_create(name=name, defaults={'description':desc})
        self.stdout.write(self.style.SUCCESS('Entitlements created/verified'))

        for role, ent_names in ROLE_MAP.items():
            for en in ent_names:
                ent = Entitlement.objects.get(name=en)
                RoleEntitlement.objects.get_or_create(role=role, entitlement=ent)
        self.stdout.write(self.style.SUCCESS('Role entitlements created/verified'))
