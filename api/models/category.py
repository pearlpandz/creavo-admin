from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default=None) # will show in list page
    short_description = models.TextField(blank=True, null=True, default=None) # will show in home page
    bg_color = models.TextField(blank=True, null=True, default=None) # solid or gradient color => #8CA2FF or linear-gradient(to right, #8CA2FF, #FF87C5)
    order = models.IntegerField(default=1000)

    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f'{self.name}'

    def __unicode__(self):
        return str(self.name)
