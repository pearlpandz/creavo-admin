from django.db import models
from django.contrib.auth.hashers import make_password
from .distributor import Distributor
from .master_distributor import MasterDistributor

class User(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    downloads = models.PositiveIntegerField(default=0) # overall downloads
    exceeded_downloads = models.PositiveIntegerField(default=0) # subscription day limit exceeded downloads
    no_subscription_downloads = models.PositiveIntegerField(default=0) # without subscription downloads
    created_by_distributor = models.ForeignKey(Distributor, on_delete=models.SET_NULL, null=True, blank=True, related_name="users_created_by_distributor")
    created_by_master_distributor = models.ForeignKey(MasterDistributor, on_delete=models.SET_NULL, null=True, blank=True, related_name="users_created_by_master_distributor")
    license = models.CharField(max_length=100, blank=True)
    purchased_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"