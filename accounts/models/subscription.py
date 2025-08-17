from django.db import models
from multiselectfield import MultiSelectField

RATING_CHOICES = (
    ('1', '1',),
    ('2', '2',),
    ('3', '3',),
    ('4', '4',),
    ('5', '5',),
)

class Subscription(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., Gold, Platinum, Diamond
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the subscription
    duration_days = models.PositiveIntegerField()  # Duration of the subscription in days
    description = models.TextField(blank=True)  # Optional description of the subscription
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the subscription was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the subscription was last updated
    daily_download_limit = models.DecimalField(default=3, max_digits=10, decimal_places=0)
    enabled_ratings = MultiSelectField(default=None, choices=RATING_CHOICES, max_length=10)
    business_cat_count = models.DecimalField(default=1, max_digits=10, decimal_places=0)
    general_cat_count = models.DecimalField(default=1, max_digits=10, decimal_places=0)
    language_cat_count = models.DecimalField(default=1, max_digits=10, decimal_places=0)
    show_trending = models.BooleanField(default=True)

    def __str__(self):
        return self.name