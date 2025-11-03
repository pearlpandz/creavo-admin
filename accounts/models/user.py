from django.db import models
from django.contrib.auth.hashers import make_password

from api.models.category import Category
from api.models.subcategory import SubCategory
from .distributor import Distributor
from .master_distributor import MasterDistributor
from django.contrib.auth.hashers import check_password

class User(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)
    date_joined = models.DateTimeField(auto_now_add=True)
    overall_downloads = models.PositiveIntegerField(default=0) # overall downloads
    day_downloads = models.PositiveIntegerField(default=0) # day downloads
    created_by_distributor = models.ForeignKey(Distributor, on_delete=models.SET_NULL, null=True, blank=True, related_name="users_created_by_distributor")
    created_by_master_distributor = models.ForeignKey(MasterDistributor, on_delete=models.SET_NULL, null=True, blank=True, related_name="users_created_by_master_distributor")
    license = models.CharField(max_length=100, blank=True)
    purchased_date = models.DateField(null=True, blank=True)
    last_login = models.DateTimeField(blank=True, null=True, default=None)
    business_category = models.ManyToManyField(SubCategory, related_name='business_category', blank=True)
    language = models.ManyToManyField(SubCategory, related_name='languages', blank=True)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

        if self.license:
            from accounts.models.license import License
            try:
                # If the license code exists, mark it as purchased
                license_obj = License.objects.get(code=self.license)
                if license_obj.status != 'purchased':
                    license_obj.status = 'purchased'
                    license_obj.purchased_by = self
                    license_obj.save(update_fields=['status', 'purchased_by'])
            except License.DoesNotExist:
                pass

    def __str__(self):                                                                                                                                                                                                                                                                                                                                                                                 
        return f"{self.first_name} {self.last_name}"

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password


class CompanyDetails(models.Model):
    media = models.FileField(upload_to='', default=None, blank=True)
    image = models.URLField(max_length=200, null=True, default=None, blank=True)
    company_name = models.CharField(max_length=50, null=True, default=None, blank=True)
    email = models.EmailField(max_length=50, null=True, default=None, blank=True)
    primary_contact = models.CharField(max_length=15, null=True, default=None, blank=True)
    secondary_contact = models.CharField(max_length=15, null=True, default=None, blank=True)
    website = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True, null=True, default=None)
    description = models.CharField(max_length=100, blank=True)
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='company_details', null=True, blank=True)  # Added

    def __str__(self):
        return f"{self.company_name}"

class Product(models.Model):
    media = models.FileField(upload_to='', default=None, blank=True)
    image = models.URLField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=25, null=True, blank=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='products', null=True, blank=True)  # Added

    def __str__(self):
        return f"{self.image}"

class Political(models.Model):
    media = models.FileField(upload_to='', null=True, default=None, blank=True)
    image = models.URLField(max_length=200, null=True, default=None, blank=True)
    leader_name = models.CharField(max_length=25)
    leader_designation = models.CharField(max_length=25, null=True, default=None, blank=True)
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='political', null=True, blank=True)  # Added

    def __str__(self):
        return f"{self.leader_name}"

class Supporters(models.Model):
    media = models.FileField(upload_to='', null=True, default=None, blank=True)
    image = models.URLField(max_length=200, null=True)
    supporter_name = models.CharField(max_length=25)
    political = models.ForeignKey('Political', on_delete=models.CASCADE, related_name='supporters', null=True, blank=True)  # Added

    def __str__(self):
        return f"{self.supporter_name}"
    

class Party(models.Model):
    party_name = models.CharField(max_length=25, null=True, default=None)
    media = models.FileField(upload_to='', default=None, blank=True)
    image = models.URLField(max_length=200, null=True, default=None)
    political = models.ForeignKey('Political', on_delete=models.CASCADE, related_name='party', null=True, blank=True)  # Added
    
    def __str__(self):
        return f"{self.party_name}"
