from django.db import models

class Subscription(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., Gold, Platinum, Diamond
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the subscription
    duration_days = models.PositiveIntegerField()  # Duration of the subscription in days
    description = models.TextField(blank=True)  # Optional description of the subscription
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the subscription was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the subscription was last updated

    def __str__(self):
        return self.name