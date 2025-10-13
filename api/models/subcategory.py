from django.db import models

class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default=None)
    category = models.ForeignKey('Category', related_name='subcategories', on_delete=models.CASCADE, default=None)
    is_active = models.BooleanField(default=True) 
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f'{self.name}'

    def __unicode__(self):
        return str(self.name)
