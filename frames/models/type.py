from django.db import models
    
class FrameType(models.Model):
    name = models.CharField(max_length=100)
    media = models.FileField(upload_to='', default=None)
    image = models.URLField(max_length=200, null=True)
    description = models.TextField(null=True, blank=True, default=None)

    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name
    