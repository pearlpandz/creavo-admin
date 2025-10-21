import os
import requests
from django.conf import settings
from django.db import models
from .category import Category
from .subcategory import SubCategory
    
class Media(models.Model):
    media = models.FileField(upload_to='', default=None)
    image = models.URLField(max_length=200, null=True)
    thumbnail = models.URLField(max_length=200, null=True)
    media_type = models.CharField(max_length=50,default='image', choices=[('image', 'Image (png, jpg, webp, gif)'), ('video', 'Video (mp4, mov, avi, mkv)')])
    title = models.CharField(max_length=100, null=True)
    short_description = models.TextField(null=True, blank=True, default=None)
    categories = models.ManyToManyField(Category, related_name='media', blank=True)
    subcategories = models.ForeignKey(SubCategory,on_delete=models.CASCADE, related_name='media', blank=True, null=True)
    rating = models.CharField(max_length=10, default=5, choices=[('1', '1'),('2', '2'),('3', '3'),('4', '4'),('5', '5')])

    REQUIRED_FIELDS = ['media', 'media_type', 'title', 'categories']

    def __str__(self):
        # Always return something printable
        return str(self.title or self.media.name or f"Media #{self.pk}")

    def save(self, *args, **kwargs):
        """
        Automatically detect file type and set image/thumbnail URLs.
        Skip sending videos to the media-service (which expects images).
        """
        base_url = getattr(settings, 'BASE_URL', 'http://127.0.0.1:8000')

        if self.media:
            ext = os.path.splitext(self.media.name)[1].lower()
            image_exts = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            video_exts = ['.mp4', '.mov', '.avi', '.mkv']

            # Detect file type
            if ext in image_exts:
                self.media_type = 'image'
            elif ext in video_exts:
                self.media_type = 'video'
            else:
                self.media_type = 'image'  # fallback

        # Save first so we have media.url
        super().save(*args, **kwargs)

        # --- Auto URL setup ---
        # Always set full image URL
        if not self.image and self.media:
            self.image = f"{base_url}{self.media.url}"

        # Handle thumbnail
        if self.media_type == 'image':
            # Optionally upload to your image processing microservice
            try:
                upload_url = "https://media-service.creavo.in/upload/media"
                with open(self.media.path, "rb") as f:
                    files = {"file": (self.media.name, f)}
                    resp = requests.post(upload_url, files=files, timeout=10)
                    if resp.status_code == 200:
                        data = resp.json()
                        # Expecting something like: {"url": "...", "thumbnail": "..."}
                        self.image = data.get("url", self.image)
                        self.thumbnail = data.get("thumbnail", self.image)
                    else:
                        # Fallback to direct URL if upload service fails
                        self.thumbnail = self.image
            except Exception as e:
                print("⚠️ Media service upload failed:", e)
                self.thumbnail = self.image

        elif self.media_type == 'video':
            # Don't upload videos to media-service
            # Use the video file itself for .image, and set thumbnail placeholder
            self.thumbnail = f"{base_url}/static/default_video_thumb.png"

        # Save again with URLs updated
        super().save(update_fields=['image', 'thumbnail'])