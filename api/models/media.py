import os
# import requests
from django.conf import settings
from django.db import models
from .category import Category
from .subcategory import SubCategory
    
class Media(models.Model):
    media = models.FileField(upload_to='', default=None)
    image = models.URLField(max_length=200, null=True)
    thumbnail = models.URLField(max_length=200, null=True)
    media_type = models.CharField(max_length=50,default=None, choices=[('image', 'Image (png, jpg, webp, gif)'), ('video', 'Video')])
    title = models.CharField(max_length=100, null=True)
    short_description = models.TextField(null=True, blank=True, default=None)
    categories = models.ManyToManyField(Category, related_name='media', blank=True)
    subcategories = models.ManyToManyField(SubCategory, related_name='media', blank=True)
    rating = models.CharField(max_length=10, default=5, choices=[('1', '1'),('2', '2'),('3', '3'),('4', '4'),('5', '5')])

    REQUIRED_FIELDS = ['media', 'media_type', 'title', 'categories']

    def __str__(self):
        return self.image
    
    def is_gif(self):
        return self.media.name.lower().endswith('.gif')
    