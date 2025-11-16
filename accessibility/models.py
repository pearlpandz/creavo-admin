from django.db import models
from core.models import User

class Entitlement(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class RoleEntitlement(models.Model):
    role = models.CharField(max_length=30, choices=User.ROLE_CHOICES)
    entitlement = models.ForeignKey(Entitlement, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'entitlement')

    def __str__(self):
        return f"{self.role} - {self.entitlement.name}"
