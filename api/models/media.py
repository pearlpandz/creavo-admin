import os
import requests
from django.conf import settings
from django.db import models
from .category import Category
from .subcategory import SubCategory
    
class Media(models.Model):
    media = models.FileField(upload_to='', default=None)
    image = models.URLField(max_length=200, null=True)
    media_type = models.CharField(max_length=50,default=None, choices=[('image', 'Image (png, jpg, webp, gif)'), ('video', 'Video')])
    title = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category, related_name='media', blank=True)
    subcategories = models.ManyToManyField(SubCategory, related_name='media', blank=True)

    REQUIRED_FIELDS = ['media', 'media_type', 'title', 'categories']

    def __str__(self):
        return self.title
    