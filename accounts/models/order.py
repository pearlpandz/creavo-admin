from django.db import models

from .master_distributor import MasterDistributor
from .distributor import Distributor
from .subscription import Subscription

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('executed', 'Executed'),
    )

    master_distributor_id = models.ForeignKey(MasterDistributor, related_name='master_distributors', on_delete=models.CASCADE, null=True, blank=True)
    distributor_id = models.ForeignKey(Distributor, related_name='distributors', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    applied_coupon = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id}"

class OrderSubscription(models.Model):
    order = models.ForeignKey(Order, related_name='subscriptions', on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
