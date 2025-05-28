from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=1000)

    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f'{self.name}'

    def __unicode__(self):
        return str(self.name)
