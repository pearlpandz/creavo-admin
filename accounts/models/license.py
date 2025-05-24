import uuid
from django.db import models
from .user import User
from .subscription import Subscription
from .distributor import Distributor
from .master_distributor import MasterDistributor

class License(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('purchased', 'Purchased'),
    ]

    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # 16-digit UUID
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="licenses")
    issued_to_distributor = models.ForeignKey(Distributor, on_delete=models.SET_NULL, null=True, blank=True, related_name="licenses")
    issued_to_master_distributor = models.ForeignKey(MasterDistributor, on_delete=models.SET_NULL, null=True, blank=True, related_name="licenses")
    purchased_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="purchased_licenses")
    purchased_at = models.DateTimeField(default=None, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.code)