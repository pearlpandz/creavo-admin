from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('retailer', 'Retailer'),
        ('distributor', 'Distributor'),
        ('master_distributor', 'Master Distributor'),
        ('super_master_distributor', 'Super Master Distributor'),
    ]

    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    phone_verified = models.BooleanField(default=False)

    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    created_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='created_users')

    def __str__(self):
        return f"{self.username} ({self.role})"

class PhoneOTP(models.Model):
    phone = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    attempts = models.IntegerField(default=0)

    def is_valid(self, expiry_seconds=300):
        from django.utils import timezone
        return (timezone.now() - self.created_at).total_seconds() < expiry_seconds

    def __str__(self):
        return f"{self.phone} - {self.otp} @ {self.created_at}"
