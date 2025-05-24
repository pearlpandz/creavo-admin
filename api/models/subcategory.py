from django.db import models

class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey('Category', related_name='subcategories', on_delete=models.CASCADE, default=None)

    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f'{self.name}'

    def __unicode__(self):
        return str(self.name)
